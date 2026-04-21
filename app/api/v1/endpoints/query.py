import logging

from fastapi import APIRouter, UploadFile, File, Depends, Request

from app.cache import semantic_cache
#from app.cache.semantic_cache import SemanticCache
from app.core.config import settings
from app.llm.base import BaseLLMProvider, LLMResponse
from app.llm.factory import get_llm_provider
from app.llm.prompts.legal import build_legal_prompt
from app.services import rag_pipeline
from app.utils.llm_formatter import LLMFormatter
#from app.services.rag_pipeline import RagPipeline
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
    # results, q_embedding = await request.app.state.rag_pipeline.query(question)
    results, q_embedding = await container.rag_pipeline.query(question)
    print('q_embedding', q_embedding)
    if not results:
        return {
            "question": question,
            "answers": []
        }
    # here results are related docs that will be context to LLM
    prompt = build_legal_prompt(question, results)
    print("PROMPT: ", prompt)
    # llm_response:LLMResponse = await llm.complete(prompt)
    llm_response:LLMResponse = await container.llm.complete(prompt)

    formatter_response = LLMFormatter.format_to_markdown(llm_response.content)
    results_normalized = [
            {
                #"answer": formatter_response["answer_markdown"],
                #"raw_answer": formatter_response["answer_text"],
                #"model": llm_response.model,
                "source": result["article"],
                "category": result["category"],
                "score": result["score"],
                #"usage": llm_response.usage,
            }
            for result in results
        ]
    ans_text = getattr(llm_response, "content", str(llm_response))
    #await request.app.state.semantic_cache.set(q_embedding, ans_text)
    # await request.app.state.semantic_cache.set_safe(q_embedding, ans_text)
    await container.semantic_cache.set_safe(q_embedding, ans_text)
    return {
        "question": question,
         "answer": formatter_response["answer_markdown"],
        # "raw_answer": formatter_response["answer_text"],
        "model": llm_response.model,
        "usage": llm_response.usage,
        "sources": results_normalized,
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