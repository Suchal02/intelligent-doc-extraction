import pytesseract
from PIL import Image, ImageFilter, ImageOps
import re
import os

# Set the tesseract command path — adjust if needed for your system
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # or where it's installed

def preprocess_image(image_path):
    image = Image.open(image_path).convert("L")      # Convert to grayscale
    image = ImageOps.invert(image)                   # Optional: Invert (for handwriting)
    image = image.filter(ImageFilter.SHARPEN)        # Sharpen image
    image = image.point(lambda x: 0 if x < 140 else 255)  # Binarize image
    return image

def clean_ocr_text(text):
    text = text.replace('\n', ' ')                         # Join newlines
    text = re.sub(r'[^\w\s.,-]', '', text)                 # Remove special/junk characters
    text = re.sub(r'\s{2,}', ' ', text)                    # Collapse multiple spaces
    return text.strip()

def ocr_image(image_path: str) -> str:
    from PIL import Image
    import pytesseract

    image = Image.open(image_path).convert("L")
    text = pytesseract.image_to_string(image)
    print("📝 OCR Output:\n", text)  # ✅ Add this
    return text

