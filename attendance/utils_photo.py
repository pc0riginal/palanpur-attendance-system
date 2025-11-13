from PIL import Image, ImageDraw, ImageFont
import io
import base64

def generate_initials_photo(name, size=200):
    """Generate a circular photo with initials"""
    try:
        # Extract initials
        name_parts = name.strip().split()
        if len(name_parts) >= 2:
            initials = name_parts[0][0].upper() + name_parts[-1][0].upper()
        else:
            initials = name_parts[0][:2].upper() if name_parts else "NA"
        
        # Create image
        img = Image.new('RGB', (size, size), color='#4A90E2')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", size//3)
        except:
            font = ImageFont.load_default()
        
        # Get text size and center it
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw text
        draw.text((x, y), initials, fill='white', font=font)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        # Return a simple colored circle as fallback
        svg_content = f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="#4A90E2"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="white" font-size="{size//3}" font-family="Arial">{initials}</text></svg>'
        return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"