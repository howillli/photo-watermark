#!/usr/bin/env python3
"""
Photo EXIF Watermark Generator

Adds a white-bordered watermark frame at the bottom of photos.
Left side: Camera brand logo + model name
Right side: Aperture | Shutter | ISO settings

Usage:
    python add_photo_watermark.py <input_image_path> [output_image_path]

Example:
    python add_photo_watermark.py photo.jpg
    python add_photo_watermark.py photo.jpg watermarked.jpg
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from PIL.ExifTags import TAGS
import re


# Brand to logo mapping
BRAND_PATTERNS = {
    'sony': ['sony', 'α', 'alpha'],
    'fujifilm': ['fujifilm', 'fuji', 'gfx', 'x-t', 'x-pro', 'x-h'],
    'nikon': ['nikon', 'z ', 'd ', 'coolpix'],
    'canon': ['canon', 'eos r', 'eos m', 'eos ', 'powershot'],
    'panasonic': ['panasonic', 'lumix', 'leica'],
    'vivo': ['vivo', 'x', 's ', 'y '],
    'apple': ['apple', 'iphone', 'ipad'],
    'huawei': ['huawei', 'p', 'mate', 'honor']
}


def get_exif_data(image_path):
    """Extract EXIF data from image file."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return None

        exif = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = value

        return exif
    except Exception as e:
        print(f"Error reading EXIF: {e}")
        return None


def parse_camera_info(exif_data):
    """Parse camera make, model, and shooting parameters from EXIF."""
    if not exif_data:
        return {
            'make': 'Unknown',
            'model': 'Unknown Camera',
            'aperture': 'N/A',
            'shutter': 'N/A',
            'iso': 'N/A'
        }

    # Get camera make and model
    make = exif_data.get('Make', '')
    model = exif_data.get('Model', '')

    # Clean up model string
    make = make.strip() if make else ''
    model = model.strip() if model else ''

    # Remove make from model if included
    if make.lower() in model.lower():
        model = re.sub(make, '', model, flags=re.IGNORECASE).strip()

    # Get aperture (FNumber)
    aperture = exif_data.get('FNumber')
    if aperture:
        try:
            if isinstance(aperture, tuple):
                aperture = aperture[0] / aperture[1] if aperture[1] != 0 else aperture[0]
            aperture = f"f/{float(aperture):.1f}"
        except:
            aperture = 'N/A'
    else:
        aperture = 'N/A'

    # Get shutter speed (ExposureTime)
    shutter = exif_data.get('ExposureTime')
    if shutter:
        try:
            if isinstance(shutter, tuple):
                numerator = shutter[0]
                denominator = shutter[1]
            else:
                numerator = shutter.numerator if hasattr(shutter, 'numerator') else shutter
                denominator = shutter.denominator if hasattr(shutter, 'denominator') else 1

            if denominator == 0:
                shutter = "N/A"
            elif denominator >= 1:
                if numerator == 1:
                    shutter = f"1/{int(denominator)}s"
                elif numerator < denominator:
                    # Format as 1/x for fractions like 10/29000
                    simplified = denominator / numerator
                    if simplified == int(simplified):
                        shutter = f"1/{int(simplified)}s"
                    else:
                        shutter = f"1/{int(denominator/numerator)}s"
                else:
                    shutter = f"1/{int(denominator/numerator)}s"
            else:
                shutter = f"{float(numerator/denominator):.1f}s"
        except:
            shutter = 'N/A'
    else:
        shutter = 'N/A'

    # Get ISO
    iso = exif_data.get('ISOSpeedRatings', exif_data.get('PhotographicSensitivity', 'N/A'))
    if iso and iso != 'N/A':
        try:
            if isinstance(iso, tuple):
                iso = str(iso[0])
            else:
                iso = str(int(iso))
            iso = f"ISO {iso}"
        except:
            iso = 'ISO N/A'
    else:
        iso = 'ISO N/A'

    return {
        'make': make,
        'model': model,
        'aperture': aperture,
        'shutter': shutter,
        'iso': iso
    }


def identify_brand(camera_info):
    """Identify camera brand from make and model."""
    full_text = f"{camera_info['make']} {camera_info['model']}".lower()

    for brand, patterns in BRAND_PATTERNS.items():
        for pattern in patterns:
            if pattern in full_text:
                return brand

    return None


def load_brand_logo(brand):
    """Load brand logo from assets."""
    if not brand:
        return None

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, '..', 'assets', 'logos', f"{brand}.png")

    if os.path.exists(logo_path):
        try:
            return Image.open(logo_path).convert('RGBA')
        except:
            return None

    return None


def create_brand_logo_svg(brand, size):
    """Create a simple SVG-based logo as fallback."""
    # Handle None brand
    if brand is None:
        brand = 'camera'
    
    brand_colors = {
        'sony': '#000000',
        'fujifilm': '#00ACE5',
        'nikon': '#FFE600',
        'canon': '#DC0019',
        'panasonic': '#003E85',
        'vivo': '#415fff',
        'apple': '#000000',
        'huawei': '#C8102E',
        'camera': '#666666'
    }

    brand_names = {
        'sony': 'SONY',
        'fujifilm': 'FUJIFILM',
        'nikon': 'NIKON',
        'canon': 'CANON',
        'panasonic': 'LUMIX',
        'vivo': 'vivo',
        'apple': '',
        'huawei': 'HUAWEI',
        'camera': 'CAM'
    }

    color = brand_colors.get(brand, '#333333')
    name = brand_names.get(brand, str(brand).upper())

    # Create a simple colored block with text
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Try to load font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size[1] // 3)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size[1] // 3)
        except:
            font = ImageFont.load_default()

    # Draw brand name or icon
    if brand == 'apple':
        # Draw apple icon-like circle
        padding = 4
        draw.ellipse([padding, padding, size[0]-padding, size[1]-padding], fill=color)
    else:
        # Draw brand name text
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2 - bbox[1]
        draw.text((x, y), name, fill=color, font=font)

    return img


def add_watermark_to_image(image_path, output_path=None, border_size=None):
    """
    Add a white-bordered watermark frame to the bottom of an image.

    Args:
        image_path: Path to input image
        output_path: Path for output (optional, defaults to <input>_watermarked.jpg)
        border_size: Height of the watermark border in pixels (default: 1/12 of image height)
    """
    # Load image
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return False

    # Fix EXIF orientation - handle rotated images
    try:
        exif = img._getexif()
        if exif:
            orientation = exif.get(274)  # 274 is Orientation tag
            if orientation == 3:
                img = img.transpose(Image.ROTATE_180)
            elif orientation == 6:
                img = img.transpose(Image.ROTATE_270)
            elif orientation == 8:
                img = img.transpose(Image.ROTATE_90)
    except:
        pass

    original_width, original_height = img.size

    # Calculate border size as 1/12 of image height if not specified
    # For portrait images, use 1/15 to avoid text crowding
    if border_size is None:
        is_portrait = original_height > original_width
        if is_portrait:
            border_size = original_height // 15
            print(f"Portrait image detected, using 1/15 border height: {border_size}")
        else:
            border_size = original_height // 12

    # Get EXIF data
    exif_data = get_exif_data(image_path)
    camera_info = parse_camera_info(exif_data)

    # Identify brand
    brand = identify_brand(camera_info)
    logo = load_brand_logo(brand)

    # Create new image with border
    new_height = original_height + border_size
    new_img = Image.new('RGB', (original_width, new_height), (255, 255, 255))
    new_img.paste(img, (0, 0))

    # Prepare drawing
    draw = ImageDraw.Draw(new_img)

    # Calculate font sizes based on border height
    left_font_size = max(24, int(border_size * 0.35))
    right_font_size = max(20, int(border_size * 0.30))

    # Load fonts - use SF Pro for better alignment with mixed text
    font_paths_regular = [
        "/System/Library/Fonts/SFNS.ttf",  # San Francisco (macOS system font)
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]

    font_paths_italic = [
        "/System/Library/Fonts/SFNSItalic.ttf",  # San Francisco Italic
        "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    ]

    left_font = None
    right_font = None  # For camera model
    params_font = None  # For parameters (italic)

    # Load regular font for camera model
    for font_path in font_paths_regular:
        try:
            left_font = ImageFont.truetype(font_path, left_font_size)
            right_font = ImageFont.truetype(font_path, right_font_size)
            break
        except:
            continue

    # Load italic font for parameters
    for font_path in font_paths_italic:
        try:
            params_font = ImageFont.truetype(font_path, right_font_size)
            break
        except:
            continue

    if left_font is None:
        left_font = ImageFont.load_default()
        right_font = left_font
    
    if params_font is None:
        params_font = right_font

    # Position logo and camera model on left
    # Get model text
    model_text = camera_info['model'] if camera_info['model'] != 'Unknown Camera' else camera_info['make']
    if model_text == 'Unknown Camera':
        model_text = 'Camera'
    
    # Calculate text metrics using actual font
    bbox = draw.textbbox((0, 0), model_text, font=left_font)
    text_height = bbox[3] - bbox[1]
    text_baseline = bbox[3]  # Bottom of text is baseline
    
    # Logo height = text height for perfect alignment
    logo_target_height = text_height
    logo_max_width = int(border_size * 2)
    
    logo_x = int(original_width * 0.03)
    
    # Calculate vertical center of border area
    border_center_y = original_height + border_size // 2

    # Load or create logo
    actual_logo_width = 0
    if logo:
        # Maintain aspect ratio while resizing
        logo_aspect = logo.width / logo.height
        target_height = logo_target_height
        target_width = int(target_height * logo_aspect)
        if target_width > logo_max_width:
            target_width = logo_max_width
            target_height = int(target_width / logo_aspect)
        
        # Resize logo
        logo = logo.resize((target_width, target_height), Image.LANCZOS)
        
        # Position logo so its vertical center aligns with text vertical center
        logo_y = border_center_y - target_height // 2
        new_img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
        actual_logo_width = target_width
    else:
        # Use fallback SVG logo
        fallback_logo = create_brand_logo_svg(brand, (logo_max_width // 2, logo_target_height))
        if fallback_logo:
            logo_y = border_center_y - logo_target_height // 2
            new_img.paste(fallback_logo, (logo_x, logo_y), fallback_logo)
            actual_logo_width = logo_max_width // 2

    # Draw camera model - position text so baseline aligns with logo center
    model_x = logo_x + actual_logo_width + 60
    model_y = border_center_y - text_height // 2 - bbox[1]
    draw.text((model_x, model_y), model_text, fill=(0, 0, 0), font=left_font)

    # Draw shooting parameters in the center
    params = f"{camera_info['aperture']} | {camera_info['shutter']} | {camera_info['iso']}"
    
    bbox = draw.textbbox((0, 0), params, font=params_font)
    params_width = bbox[2] - bbox[0]
    params_height = bbox[3] - bbox[1]
    
    # Center horizontally
    params_x = (original_width - params_width) // 2
    params_y = border_center_y - params_height // 2 - bbox[1]
    
    draw.text((params_x, params_y), params, fill=(100, 100, 100), font=params_font)
    
    # Draw author and date on the right
    from datetime import datetime
    now = datetime.now()
    author_text = f"mingshu, {now.year}.{now.month:02d}"
    
    bbox_author = draw.textbbox((0, 0), author_text, font=params_font)
    author_width = bbox_author[2] - bbox_author[0]
    author_height = bbox_author[3] - bbox_author[1]
    
    author_x = original_width - author_width - int(original_width * 0.03)
    author_y = border_center_y - author_height // 2 - bbox_author[1]
    
    draw.text((author_x, author_y), author_text, fill=(100, 100, 100), font=params_font)

    # Save output
    if not output_path:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_watermarked.jpg"

    try:
        # Preserve EXIF if possible
        new_img.save(output_path, 'JPEG', quality=95, optimize=True)
        print(f"Watermarked image saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python add_photo_watermark.py <input_image> [output_image]")
        print("Example: python add_photo_watermark.py photo.jpg")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    success = add_watermark_to_image(input_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
