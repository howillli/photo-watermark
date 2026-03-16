#!/usr/bin/env python3
"""
Generate brand logos for the photo watermark skill.
Creates PNG logos for: Sony, Fujifilm, Nikon, Canon, Panasonic, Vivo, Apple, Huawei
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_sony_logo(size):
    """Create Sony logo - simple SONY text in black."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.5))
    except:
        font = ImageFont.load_default()
    
    text = "SONY"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    return img


def create_fujifilm_logo(size):
    """Create Fujifilm logo - blue hexagon with F."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw hexagon
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = min(size) // 2 - 5
    
    points = []
    for i in range(6):
        angle = i * 60 * 3.14159 / 180
        px = center_x + radius * 0.8 * (1 if i in [0, 3] else 0.5 if i in [1, 5] else -0.5)
        py = center_y + radius * (0 if i in [0, 3] else 0.866 if i in [1, 2] else -0.866)
        points.append((px, py))
    
    # Simple circle for hexagon approximation
    draw.ellipse([5, 5, size[0]-5, size[1]-5], fill=(0, 172, 229, 255))  # Fujifilm blue
    
    # Draw "F" in white
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.5))
    except:
        font = ImageFont.load_default()
    
    text = "F"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    return img


def create_nikon_logo(size):
    """Create Nikon logo - yellow background with black text."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Yellow background
    draw.ellipse([2, 2, size[0]-2, size[1]-2], fill=(255, 230, 0, 255))
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.35))
    except:
        font = ImageFont.load_default()
    
    text = "NIKON"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    return img


def create_canon_logo(size):
    """Create Canon logo - red text."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.45))
    except:
        font = ImageFont.load_default()
    
    text = "Canon"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    # Canon red
    draw.text((x, y), text, fill=(220, 0, 25, 255), font=font)
    return img


def create_panasonic_logo(size):
    """Create Panasonic/Lumix logo - blue text."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.3))
    except:
        font = ImageFont.load_default()
    
    text = "LUMIX"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    # Panasonic blue
    draw.text((x, y), text, fill=(0, 62, 133, 255), font=font)
    return img


def create_vivo_logo(size):
    """Create Vivo logo - blue circle with white V."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Blue circle
    draw.ellipse([3, 3, size[0]-3, size[1]-3], fill=(65, 95, 255, 255))
    
    # White "v" in center
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.4))
    except:
        font = ImageFont.load_default()
    
    text = "vivo"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    return img


def create_apple_logo(size):
    """Create Apple logo - simple bitten apple shape."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple circle to represent apple icon
    padding = 4
    draw.ellipse([padding, padding, size[0]-padding, size[1]-padding], fill=(0, 0, 0, 255))
    
    # Add a small bite mark
    draw.ellipse([size[0]*0.7, size[1]*0.3, size[0]*0.9, size[1]*0.5], fill=(255, 255, 255, 0))
    
    return img


def create_huawei_logo(size):
    """Create Huawei logo - red text."""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size[1] * 0.35))
    except:
        font = ImageFont.load_default()
    
    text = "HUAWEI"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - bbox[1]
    
    # Huawei red
    draw.text((x, y), text, fill=(200, 16, 46, 255), font=font)
    return img


def main():
    logos_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logos')
    os.makedirs(logos_dir, exist_ok=True)
    
    size = (100, 100)  # Logo size
    
    logos = {
        'sony': create_sony_logo,
        'fujifilm': create_fujifilm_logo,
        'nikon': create_nikon_logo,
        'canon': create_canon_logo,
        'panasonic': create_panasonic_logo,
        'vivo': create_vivo_logo,
        'apple': create_apple_logo,
        'huawei': create_huawei_logo
    }
    
    for name, func in logos.items():
        logo = func(size)
        output_path = os.path.join(logos_dir, f"{name}.png")
        logo.save(output_path, 'PNG')
        print(f"Created {name}.png")
    
    print(f"\nAll logos created in: {logos_dir}")


if __name__ == "__main__":
    main()
