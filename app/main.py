import logging

from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import setup_logger

# ============= initialize logger ONCE when app starts
setup_logger(settings.app_name)

# ======== USE Logger ===========
logger = logging.getLogger(settings.app_name)

app = FastAPI(
    title="RAG System API",
    description="Pocket Attorney RAG System API",
    version="1.0.0",
)


app.include_router(api_router, prefix="/api/v1")

# quick health check

@app.get("/")
async def root():
    return {"status": "ok", "message": "Pocket Attorney RAG System API is running"}


# ========= APP EVENTS ================
@app.on_event("startup")
async def startup():
    logger.info("Pocket Attorney RAG System API is running")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Pocket Attorney RAG System API is shutting down")


#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
