# Asset Processor 🎮

A Python tool for automatic preprocessing of 2D assets (images), designed for **game development pipelines** 

The goal is to automate repetitive steps in asset preparation before importing them into a game engine or internal tools:

- automatic resizing of images  
- format conversion (e.g., JPG → PNG)  
- consistent renaming  
- generation of `metadata.json` with all relevant asset information  

---

## 🎯 Why this project is relevant for game development

In mobile game studios, similar tools are used every day to:

- normalize sprites and UI assets to a standard size and format  
- reduce asset weight before the build pipeline  
- generate metadata for engines, build systems, and level editors  
- support artists and game designers by automating repetitive manual tasks  

This project demonstrates experience in:

- **Python scripting for internal development tools**  
- image preprocessing using `Pillow`  
- designing a **CLI** usable by other team members  
- structuring code as a reusable package  

---

## 🧱 Project Structure

    asset-processor/
    ├─ assets_raw/          # input: source images
    ├─ assets_processed/    # output: processed images + metadata.json
    ├─ src/
    │  └─ asset_processor/
    │     ├─ __init__.py
    │     └─ main.py
    ├─ README.md
    ├─ requirements.txt
    └─ .gitignore

---

## 🛠 Tech Stack

- **Language**: Python 3  
- **Key libraries**:  
  - `Pillow` for image manipulation  
  - `argparse` for the command-line interface  
  - `pathlib` & `json` for filesystem and metadata management  

---

## 🚀 Installation

Requires **Python 3.10+**.

    git clone https://github.com/Ramonster98/asset-processor.git
    cd asset-processor

    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate

    pip install -r requirements.txt

---

## ▶️ Usage

### Basic execution (uses default folders `assets_raw` → `assets_processed`)

    python src/asset_processor/main.py

### With parameters

Windows (PowerShell or CMD):

    python src/asset_processor/main.py ^
      --input-dir assets_raw ^
      --output-dir assets_processed ^
      --width 512 ^
      --height 512 ^
      --format png ^
      --quality 85

macOS/Linux:

    python src/asset_processor/main.py \
      --input-dir assets_raw \
      --output-dir assets_processed \
      --width 512 \
      --height 512 \
      --format png \
      --quality 85

| Parameter | Description |
|----------|-------------|
| `--input-dir` | Folder containing the original images |
| `--output-dir` | Output folder |
| `--width`, `--height` | Target dimensions. If only one is provided, the other is calculated to preserve aspect ratio |
| `--format` | Output format (`png`, `jpg`, …). If omitted, keeps original |
| `--quality` | JPG quality (1–95), default: 85 |

**Output:**

- processed images in the output folder  
- `metadata.json` containing, for each asset:  
  - source file  
  - output file  
  - width  
  - height  
  - size in bytes  
  - format  

---

## 🧪 Example Commands

Resize all assets to width 512px while preserving aspect ratio:

    python src/asset_processor/main.py --width 512 --format png

Resize to 512×512 and convert to JPG with reduced size:

    python src/asset_processor/main.py --width 512 --height 512 --format jpg --quality 75

Use custom input/output folders:

    python src/asset_processor/main.py --input-dir raw_assets --output-dir optimized_assets

---

## 🧭 Roadmap

- [x] Base CLI for image preprocessing  
- [x] Resize with aspect-ratio handling  
- [x] Format conversion + adjustable JPG quality  
- [x] JSON metadata export  
- [ ] Structured logging (for integration in larger pipelines)  
- [ ] External configuration file (e.g., `config.json` or `.yaml`)  
- [ ] Automated tests (`pytest`)  
- [ ] Package the tool (`pip install .`)  
- [ ] Integration with a sample engine or level editor  

---

## 💼 Skills demonstrated

- Python scripting for internal development tools  
- Preprocessing of 2D game assets  
- Command-line tool design for production workflows  
- Clean project structure (`src/` layout)  
- Git & GitHub for version control and collaboration  
