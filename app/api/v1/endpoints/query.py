import logging

from fastapi import APIRouter, UploadFile, File, Depends

from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.factory import get_llm_provider
from app.llm.prompts.legal import build_legal_prompt
from app.services.rag_pipeline import RagPipeline
from app.utils.utility import extract_pdf_text, clean_text

logger = logging.getLogger(settings.app_name)

router = APIRouter()
rag = RagPipeline()

@router.get("/hello")
async def hello_world():
    return {"message": "Hello Ishmael"}

@router.post("/ask")
async def ask_question(payload: dict, llm: BaseLLMProvider = Depends(get_llm_provider)):
    question = payload.get("question")
    results = rag.query(question)

    if not results:
        return {
            "question": question,
            "answers": []
        }
    # here results are related docs that will be context to LLM
    prompt = build_legal_prompt(question, results)
    print("PROMPT: ", prompt)
    ans = await llm.complete(prompt)
    print("ANS: ", ans)

    return {
        "question": question,
        "answers": [
            {
                "answer": result["answer"],
                "source": result["article"],
                "category": result["category"],
                "score": result["score"]
            }
            for result in results
        ]
    }


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Upload file {file.filename}")
    file_bytes = await file.read()
    text = extract_pdf_text(file_bytes)
    # print(text)
    sanitized = clean_text(text)
    print(sanitized)
    return {
        "filename": file.filename,
        "length": len(text),
    }