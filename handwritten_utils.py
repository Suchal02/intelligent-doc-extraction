import pytesseract
from PIL import Image
import re

def extract_handwritten_text(image_path: str) -> str:
    image = Image.open(image_path).convert("L")
    return pytesseract.image_to_string(image)

def extract_fields_from_text(text: str, instruction: str) -> dict:
    instruction = instruction.lower()
    result = {}

    clean_text = text.lower()

    if "client name" in instruction:
        match = re.search(r"name[:\-]?\s*([a-zA-Z\s]{3,})", clean_text)
        if match:
            result["Client Name"] = match.group(1).strip()

    if "action item" in instruction:
        items = re.findall(r"(?:action item[:\-]?\s*)(.*?)(?:\\n|$)", clean_text)
        if items:
            result["Action Items"] = [i.strip() for i in items if i.strip()]

    if not result:
        result["message"] = "❌ No matching fields found."
        result["raw_text"] = text

    return result
