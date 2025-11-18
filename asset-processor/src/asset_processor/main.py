import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional

from PIL import Image

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Processa asset grafici (resize, conversione formato, metadati)."
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="assets_raw",
        help="Cartella di input con le immagini originali (default: assets_raw).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="assets_processed",
        help="Cartella di output per le immagini processate (default: assets_processed).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Larghezza target (px). Se non specificata, mantiene l'originale o calcola in base all'altezza.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Altezza target (px). Se non specificata, mantiene l'originale o calcola in base alla larghezza.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default=None,
        help="Formato di output (es. png, jpg). Di default mantiene il formato originale.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="Qualità per il formato JPG (1-95, default: 85).",
    )
    return parser.parse_args()


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def collect_images(input_dir: Path) -> List[Path]:
    images: List[Path] = []
    for path in input_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(path)
    return images


def process_image(
    src_path: Path,
    dest_dir: Path,
    width: Optional[int],
    height: Optional[int],
    out_format: Optional[str],
    quality: int,
) -> Dict:
    with Image.open(src_path) as img:
        original_width, original_height = img.size

        # Calcolo nuova dimensione
        if width is None and height is None:
            new_width, new_height = original_width, original_height
        else:
            if width is None:
                ratio = height / float(original_height)
                new_width = int(original_width * ratio)
                new_height = height
            elif height is None:
                ratio = width / float(original_width)
                new_width = width
                new_height = int(original_height * ratio)
            else:
                new_width, new_height = width, height

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Decidi formato di salvataggio
        ext = src_path.suffix.lower()
        if out_format:
            save_format = out_format.lower()
        else:
            save_format = ext.lstrip(".")

        output_filename = src_path.stem + f".{save_format}"
        output_path = dest_dir / output_filename

        save_kwargs = {}
        if save_format in ("jpg", "jpeg"):
            save_kwargs["quality"] = quality

        img.save(output_path, save_format.upper(), **save_kwargs)

    file_size = output_path.stat().st_size

    return {
        "source_file": str(src_path),
        "output_file": str(output_path),
        "width": new_width,
        "height": new_height,
        "size_bytes": file_size,
        "format": save_format,
    }


def main() -> None:
    args = parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Cartella di input non valida: {input_dir}")

    ensure_output_dir(output_dir)

    images = collect_images(input_dir)
    if not images:
        print(f"Nessuna immagine trovata in {input_dir}")
        return

    print(f"Trovate {len(images)} immagini. Inizio processamento...\n")

    metadata: List[Dict] = []

    for img_path in images:
        print(f"  → Processando: {img_path}")
        info = process_image(
            src_path=img_path,
            dest_dir=output_dir,
            width=args.width,
            height=args.height,
            out_format=args.format,
            quality=args.quality,
        )
        metadata.append(info)

    metadata_path = output_dir / "metadata.json"
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"\nCompletato. Metadati salvati in: {metadata_path}")


if __name__ == "__main__":
    main()
