from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from docx2pdf import convert
import tempfile
import shutil
import os

app = FastAPI()

@app.post("/convert-docx-to-pdf")
async def convert_docx_to_pdf(request: Request):
    # Save incoming binary to a temp .docx file
    docx_bytes = await request.body()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        tmp_docx.write(docx_bytes)
        tmp_docx_path = tmp_docx.name

    tmp_pdf_path = tmp_docx_path.replace(".docx", ".pdf")

    try:
        convert(tmp_docx_path, tmp_pdf_path)
        return StreamingResponse(open(tmp_pdf_path, "rb"), media_type="application/pdf")
    finally:
        os.remove(tmp_docx_path)
        if os.path.exists(tmp_pdf_path):
            os.remove(tmp_pdf_path)
