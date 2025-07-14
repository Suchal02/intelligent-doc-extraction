# app/nlp_parser_utils.py
from transformers import pipeline

RISK_KEYWORDS = [
    "penalty", "termination", "breach", "liable", "failure to pay",
    "late fee", "interest", "non-compliance", "termination for cause",
    "liquidated damages", "indemnity", "dispute", "arbitration", "lawsuit"
] 

try:
    from transformers import pipeline
    summarizer = pipeline("text2text-generation", model="google/flan-t5-small")
    USE_FLAN = True
except:
    USE_FLAN = False

def parse_instruction(instruction, text):
    instruction = instruction.lower()
    results = []

    if "effective date" in instruction:
        import re
        results = re.findall(r"\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b", text)

    elif "party" in instruction or "party name" in instruction:
        lines = text.split("\n")
        results = [line for line in lines if "party" in line.lower()]

    elif "termination" in instruction:
        results = [line for line in text.split("\n") if "termination" in line.lower()]

    elif "penalty" in instruction:
        results = [line for line in text.split("\n") if "penalty" in line.lower()]

    elif "explain" in instruction or "summarize" in instruction:
        results = [line for line in text.split("\n") if len(line.strip()) > 20]
    
    elif "attribute" in instruction.lower():
        return extract_keyword(text, "attribute")


    else:
        results = ["No matching instruction parser. Showing full text...", text]

    return "\n".join(results)


def extract_keyword(keyword, text):
    keyword = keyword.lower()
    lines = text.split("\n")
    matches = [line for line in lines if keyword in line.lower()]
    return "\n".join(matches) if matches else f"No lines found for keyword '{keyword}'."

def flag_risky_clauses(text):
    flagged = []
    for line in text.split('\n'):
        for keyword in RISK_KEYWORDS:
            if keyword.lower() in line.lower():
                flagged.append(line.strip())
                break
    return flagged
