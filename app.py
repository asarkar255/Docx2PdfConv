from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import tempfile
import subprocess
import shutil
import os

app = FastAPI()

@app.post("/convert-docx-to-pdf")
async def convert_docx_to_pdf(request: Request):
    docx_bytes = await request.body()

    # Save input .docx to a temp file
    with tempfile.TemporaryDirectory() as tmp_dir:
        docx_path = os.path.join(tmp_dir, "input.docx")
        pdf_path = os.path.join(tmp_dir, "input.pdf")

        with open(docx_path, "wb") as f:
            f.write(docx_bytes)

        # Convert using LibreOffice in headless mode
        try:
            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", tmp_dir,
                docx_path
            ], check=True)

            # Return the PDF as a stream
            return StreamingResponse(
                open(pdf_path, "rb"),
                media_type="application/pdf",
                headers={"Content-Disposition": "inline; filename=converted.pdf"}
            )

        except subprocess.CalledProcessError as e:
            return {"error": f"LibreOffice conversion failed: {str(e)}"}
