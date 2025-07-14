from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch
import csv
import os

# Load model + processor once
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
model = LlavaForConditionalGeneration.from_pretrained(
    "llava-hf/llava-1.5-7b-hf", torch_dtype=torch.float16, device_map="auto"
)

def process_vlm_image(image_path: str, instruction: str) -> dict:
    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=instruction, images=image, return_tensors="pt").to("cpu")
    generate_ids = model.generate(**inputs, max_new_tokens=300)
    generated_text = processor.batch_decode(generate_ids, skip_special_tokens=True)[0]

    # Save to CSV
    csv_path = "outputs/vlm_output.csv"
    os.makedirs("outputs", exist_ok=True)
    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Extracted Information"])
        writer.writerow([generated_text])

    return {
        "output": generated_text,
        "csv_path": csv_path
    }
