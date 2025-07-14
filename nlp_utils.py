from transformers import pipeline
import os
from dotenv import load_dotenv
load_dotenv()

model = os.getenv("MODEL_FLAN")
parser = pipeline("text2text-generation", model=model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def parse_instruction(text):
    return parser(text)[0]["generated_text"]

def generate_summary(text: str) -> str:
    text = text[:4000]  # Limit input length for model
    result = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return result[0]['summary_text']