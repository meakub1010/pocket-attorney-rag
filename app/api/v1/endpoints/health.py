from fastapi import APIRouter, Depends

from app.llm.base import BaseLLMProvider
from app.llm.factory import get_llm_provider

router = APIRouter()


@router.get("/status")
async def status(llm: BaseLLMProvider = Depends(get_llm_provider)):
    print(llm)
    return {"status": "OK"}
