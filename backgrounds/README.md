# 🎨 Color Extractor

A Python script that extracts dominant colors from images using K-means clustering and displays them both in the terminal and as PNG palette files.

## ✨ Features

- Extract dominant colors from any image format (JPG, PNG, etc.)
- Display colors visually in the terminal with ANSI color codes
- Generate PNG palette files with hex codes
- Save color information to text files
- Customizable number of colors to extract
- Cross-platform support (Linux, macOS, Windows)

## 📦 Dependencies

Install the required packages:

```bash
pip install pillow numpy scikit-learn
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pillow>=9.0.0
numpy>=1.21.0
scikit-learn>=1.0.0
```

## 🚀 Usage

### Basic Usage

```bash
# Extract 5 colors (default) from an image
python color_extractor.py image.jpg

# Or use the wrapper script (Linux)
./run_color_extractor.sh image.jpg
```

### Command Line Options

```bash
python color_extractor.py <image_path> [OPTIONS]
```

**Options:**
- `-n, --num-colors`: Number of colors to extract (default: 5)
- `-s, --save`: Save palette to text file
- `-o, --open`: Create PNG palette and open it automatically
- `--output`: Custom output filename for text palette

### Examples

```bash
# Extract 3 colors
python color_extractor.py image.jpg -n 3

# Extract 10 colors
python color_extractor.py image.jpg --num-colors 10

# Extract colors and save to text file
python color_extractor.py image.jpg -s

# Extract colors and open PNG palette
python color_extractor.py image.jpg -o

# Extract 8 colors, save text file, and open PNG
python color_extractor.py image.jpg -n 8 -s -o

# Custom text output filename
python color_extractor.py image.jpg -s --output my_colors.txt
```

## 📁 Output Files

The script generates the following files:

- **PNG Palette**: `<image_name>_palette.png` - Visual color palette with hex codes
- **Text File** (optional): `<image_name>_palette.txt` - Detailed color information

## 🖼️ Sample Output

**Terminal Output:**
```
🎨 Color Palette (5 colors):
============================================================
1. [COLOR_BLOCK] RGB: (45, 87, 123)
   [COLOR_BLOCK] HEX: #2d577b
   [COLOR_BLOCK] Frequency: 32.4%

2. [COLOR_BLOCK] RGB: (200, 180, 160)
   [COLOR_BLOCK] HEX: #c8b4a0
   [COLOR_BLOCK] Frequency: 28.1%
...
```

**PNG Palette:**
A horizontal bar showing the extracted colors with their hex codes overlaid.

## 🐧 Linux Setup (Optional)

For Linux users, use the included wrapper script that sets proper locale and color support:

```bash
# Make the script executable
chmod +x run_color_extractor.sh

# Run with proper environment
./run_color_extractor.sh image.jpg -n 8 -o
```

## 🔧 Technical Details

- **Algorithm**: K-means clustering to find dominant colors
- **Color Space**: RGB color space
- **Terminal Colors**: 24-bit ANSI color codes (truecolor support required)
- **Image Processing**: PIL/Pillow for image handling
- **Clustering**: scikit-learn KMeans implementation

## 🎯 Use Cases

- **Web Design**: Extract color palettes for websites
- **Art Projects**: Analyze color schemes in artwork
- **Brand Analysis**: Extract brand colors from logos
- **Color Inspiration**: Generate palettes from photographs
- **Design Systems**: Create consistent color schemes

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

*Perfect for designers, developers, and anyone who loves working with colors!* 🌈
