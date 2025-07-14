from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from app.nlp_utils import generate_summary
from app.ocr_utils import ocr_image
from app.nlp_parser_utils import parse_instruction
from app.table_utils import extract_all_tables
from app.extractor import extract_pdf_text
from app.vlm_utils import process_vlm_image
from app.handwritten_utils import extract_fields_from_text
from app.legal_utils import extract_legal_fields

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp_files", exist_ok=True)

@app.post("/extract-text/")
async def extract_text(file: UploadFile = ..., instruction: str = Form(...)):
    try:
        file_path = f"temp_files/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = {"instruction": instruction}
        extracted_text = ""

        # 🖼️ Image files (diagrams or handwriting)
        if file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
            extracted_text = ocr_image(file_path)

            if "diagram" in instruction.lower() or "blueprint" in instruction.lower():
                vlm_output = process_vlm_image(file_path, instruction)
                results.update(vlm_output)
            else:
                fields = extract_fields_from_text(extracted_text, instruction)
                results["output"] = fields

        # 📄 PDF documents (contracts, tables)
        elif file.filename.lower().endswith(".pdf"):
            extracted_text, pages = extract_pdf_text(file_path)
            summary = generate_summary(extracted_text)
            results["summary"] = summary
            extracted_fields, flagged = extract_legal_fields(extracted_text, instruction)
            results["output"] = extracted_fields
            results["flagged"] = flagged

            # ✅ Always run table extraction
            tables = extract_all_tables(file_path)
            results["tables"] = tables

        return JSONResponse(content=results)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
