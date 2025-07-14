import re

def extract_legal_fields(text: str, instruction: str):
    instruction = instruction.lower()
    output = {}
    flagged = []

    if "effective date" in instruction:
        match = re.search(r"effective date[:\-]?\s*(\w+\s\d{1,2},\s\d{4})", text, re.IGNORECASE)
        if match:
            output["Effective Date"] = match.group(1)

    if "party name" in instruction or "parties" in instruction:
        parties = re.findall(r"between\s+(.*?)\s+and\s+(.*?)[.,\\n]", text, re.IGNORECASE)
        if parties:
            output["Parties"] = {"Party A": parties[0][0], "Party B": parties[0][1]}

    if "termination clause" in instruction:
        clause = re.findall(r"(termination[^\\n\\.]{0,500})", text, re.IGNORECASE | re.DOTALL)
        if clause:
            output["Termination Clause"] = f"**{clause[0].strip()}**"
            if "ambiguous" in clause[0].lower() or "discretion" in clause[0].lower():
                flagged.append("⚠️ Termination clause contains vague language")

    if "penalty clause" in instruction or "penalties" in instruction:
        penalties = re.findall(r"(penalt(y|ies)[^\\n\\.]{0,500})", text, re.IGNORECASE | re.DOTALL)
        if penalties:
            output["Penalty Clause"] = penalties[0][0]
            if "subjective" in penalties[0][0].lower() or "may include" in penalties[0][0].lower():
                flagged.append("⚠️ Penalty clause may be non-specific")

    if not output:
        output["message"] = "❌ No matching clauses found for instruction."

    return output, flagged
