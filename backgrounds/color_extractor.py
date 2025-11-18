import sys
import argparse
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import os

class ColorExtractor:
    def __init__(self, image_path, num_colors=5):
        self.image_path = image_path
        self.num_colors = num_colors
        self.image = None
        
    def load_image(self):
        """Load and process the image"""
        try:
            self.image = Image.open(self.image_path)
            # Convert to RGB if necessary
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')
            print(f"Loaded image: {self.image_path}")
            print(f"Image size: {self.image.size}")
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def extract_colors(self):
        """Extract dominant colors using K-means clustering"""
        if not self.image:
            print("No image loaded!")
            return []
        
        # Convert image to numpy array
        img_array = np.array(self.image)
        
        # Reshape to list of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Use K-means to find dominant colors
        kmeans = KMeans(n_clusters=self.num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the colors and their frequencies
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        
        # Count frequency of each color
        label_counts = Counter(labels)
        
        # Sort colors by frequency
        color_info = []
        for i, color in enumerate(colors):
            frequency = label_counts[i] / len(labels) * 100
            color_info.append({
                'rgb': tuple(int(c) for c in color),  # Convert numpy ints to Python ints
                'hex': self.rgb_to_hex(color),
                'frequency': frequency
            })
        
        # Sort by frequency (most common first)
        color_info.sort(key=lambda x: x['frequency'], reverse=True)
        
        return color_info
    
    def rgb_to_hex(self, rgb):
        """Convert RGB values to hex color code"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def rgb_to_ansi(self, rgb):
        """Convert RGB to ANSI 24-bit color code for terminal display"""
        r, g, b = rgb
        return f"\033[48;2;{r};{g};{b}m"
    
    def reset_color(self):
        """Reset terminal color"""
        return "\033[0m"
    
    def display_colors(self, colors):
        """Display the extracted colors with visual blocks in terminal"""
        print(f"\nColor Palette ({len(colors)} colors):")
        print("=" * 60)
        
        for i, color in enumerate(colors, 1):
            rgb = color['rgb']
            hex_code = color['hex']
            freq = color['frequency']
            
            # Create color swatch
            color_swatch = self.rgb_to_ansi(rgb) + "          " + self.reset_color()
            
            print(f"{i}. {color_swatch} RGB: {rgb}")
            print(f"   {color_swatch} HEX: {hex_code}")
            print(f"   {color_swatch} Frequency: {freq:.1f}%")
            print()
    
    def create_color_palette_image(self, colors, output_path=None):
        """Create a visual color palette image"""
        if not output_path:
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            output_path = f"{base_name}_palette.png"
        
        # Create palette image
        palette_width = 800
        palette_height = 100
        
        # Create image
        palette_img = Image.new('RGB', (palette_width, palette_height))
        draw = ImageDraw.Draw(palette_img)
        
        # Calculate width for each color
        color_width = palette_width // len(colors)
        
        # Draw color rectangles
        for i, color in enumerate(colors):
            x1 = i * color_width
            x2 = (i + 1) * color_width
            rgb = color['rgb']
            
            # Draw rectangle
            draw.rectangle([x1, 0, x2, palette_height], fill=rgb)
            
            # Add text with hex code
            text = color['hex']
            text_bbox = draw.textbbox((0, 0), text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Position text in center of rectangle
            text_x = x1 + (color_width - text_width) // 2
            text_y = (palette_height - text_height) // 2
            
            # Choose text color based on background brightness
            brightness = sum(rgb) / 3
            text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
            
            draw.text((text_x, text_y), text, fill=text_color)
        
        # Save palette image
        palette_img.save(output_path)
        print(f"Color palette saved as: {output_path}")
        
        return output_path
    
    def show_palette(self, palette_path):
        """Open the color palette image"""
        try:
            if sys.platform.startswith('linux'):
                os.system(f'xdg-open "{palette_path}"')
            elif sys.platform.startswith('darwin'):  # macOS
                os.system(f'open "{palette_path}"')
            elif sys.platform.startswith('win'):
                os.system(f'start "{palette_path}"')
            print(f"👀 Opening color palette: {palette_path}")
        except Exception as e:
            print(f"Could not open palette image: {e}")
    
    def save_palette(self, colors, output_file=None):
        """Save color palette to a file"""
        if not output_file:
            output_file = f"{self.image_path.split('.')[0]}_palette.txt"
        
        try:
            with open(output_file, 'w') as f:
                f.write(f"Color Palette for: {self.image_path}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, color in enumerate(colors, 1):
                    f.write(f"Color {i}:\n")
                    f.write(f"  RGB: {color['rgb']}\n")
                    f.write(f"  HEX: {color['hex']}\n")
                    f.write(f"  Frequency: {color['frequency']:.1f}%\n\n")
            
            print(f"💾 Palette saved to: {output_file}")
        except Exception as e:
            print(f"Error saving palette: {e}")

def main():
    parser = argparse.ArgumentParser(description='Extract color scheme from an image')
    parser.add_argument('image', help='Path to the image file')
    parser.add_argument('-n', '--num-colors', type=int, default=5, 
                       help='Number of colors to extract (default: 5)')
    parser.add_argument('-s', '--save', action='store_true', 
                       help='Save palette to text file')
    parser.add_argument('-o', '--open', action='store_true',
                       help='Create PNG palette and open it automatically')
    parser.add_argument('--output', type=str, 
                       help='Output file name for saved text palette')
    
    args = parser.parse_args()
    
    # Create color extractor
    extractor = ColorExtractor(args.image, args.num_colors)
    
    # Load image
    if not extractor.load_image():
        sys.exit(1)
    
    # Extract colors
    print(f"Extracting {args.num_colors} dominant colors...")
    colors = extractor.extract_colors()
    
    if colors:
        # Display colors
        extractor.display_colors(colors)
        
        # Always create PNG palette
        palette_path = extractor.create_color_palette_image(colors)
        
        # Only open PNG if -o flag is provided
        if args.open:
            extractor.show_palette(palette_path)
        
        # Save text palette if requested
        if args.save:
            extractor.save_palette(colors, args.output)
    else:
        print("Failed to extract colors!")
        sys.exit(1)

if __name__ == "__main__":
    main()