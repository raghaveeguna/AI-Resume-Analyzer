
import pymupdf
import docx
from io import BytesIO

async def parse_resume(file: UploadFile) -> str:
    content = await file.read()
    text = ""
    if file.content_type == "application/pdf":
        with pymupdf.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(BytesIO(content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file.content_type == "text/plain":
        text = content.decode("utf-8")
    return text
