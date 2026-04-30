import logging

from fastapi import APIRouter, UploadFile, File, Depends, Request

from app.core.config import settings
from app.utils.utility import extract_pdf_text, clean_text

logger = logging.getLogger(settings.app_name)

router = APIRouter()

def get_container(request: Request):
    return request.app.state.container

@router.get("/hello")
async def hello_world():
    return {"message": "Hello Ishmael"}

@router.post("/ask")
async def ask_question(payload: dict, container = Depends(get_container)):
    question = payload.get("question")
    return await container.query_service.ask(question)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Upload file {file.filename}")
    file_bytes = await file.read()
    text = extract_pdf_text(file_bytes)
    sanitized = clean_text(text)
    print(sanitized)
    return {
        "filename": file.filename,
        "length": len(text),
    }