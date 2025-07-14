import pdfplumber
from docx import Document
def extract_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([p.extract_text() or "" for p in pdf.pages])

def extract_pdf_tables(file_path):
    all_tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)
    return all_tables



def extract_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

import re

# Simple keyword-based clause extractor
def extract_legal_fields(text: str, instruction: str):
    instruction = instruction.lower()
    output = {}
    flagged = []

    if "effective date" in instruction:
        match = re.search(r"effective date[:\-]?\s*(\w+\s\d{1,2},\s\d{4})", text, re.IGNORECASE)
        if match:
            output["Effective Date"] = match.group(1)

    if "party name" in instruction or "parties" in instruction:
        parties = re.findall(r"between\s+(.*?)\s+and\s+(.*?)[.,\n]", text, re.IGNORECASE)
        if parties:
            output["Parties"] = {"Party A": parties[0][0], "Party B": parties[0][1]}

    if "termination clause" in instruction:
        clause = re.findall(r"(termination.*?)(?=\\n[A-Z ]{2,}|\\Z)", text, re.IGNORECASE | re.DOTALL)
        if clause:
            output["Termination Clause"] = clause[0]
            if "ambiguous" in clause[0].lower() or "discretion" in clause[0].lower():
                flagged.append("Termination clause contains vague language")

    if "penalty clause" in instruction or "penalties" in instruction:
        penalties = re.findall(r"(penalt(y|ies).*?)(?=\\n[A-Z ]{2,}|\\Z)", text, re.IGNORECASE | re.DOTALL)
        if penalties:
            output["Penalty Clause"] = penalties[0][0]
            if "subjective" in penalties[0][0].lower() or "may include" in penalties[0][0].lower():
                flagged.append("Penalty clause may be non-specific")

    if not output:
        output["message"] = "No matching clauses found for instruction."

    return output, flagged
