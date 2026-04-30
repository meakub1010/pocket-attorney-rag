import json
import os

from rank_bm25 import BM25Okapi

from app.services.bm25_store import BM25Store
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore

# run this script using below command
# uv run python -m app.ingestion.build_index
# script has been registered as project.scripts in toml


def build_index(data_path: str, save_path: str):
    embedder = EmbeddingService()
    chunker = get_chunker()

    with open(data_path) as f:
        data = json.load(f)

    chunks = []
    metadata = []

    for item in data:
        text = f"""
                    {item["article"]}
                    {item["title"]}
                    {item["text"]}
                    """
        doc_chunks = chunker.split(text)
        for chunk in doc_chunks:
            chunks.append(chunk)
            metadata.append(
                {
                    "chunk": chunk,
                    "keywords": item.get("keywords", []),
                    "article": item["article"],
                    "title": item["title"],
                    "category": item["category"],
                }
            )
    # embeddings = embedder.embed(chunks) # update to embed_batch
    # vector_store = VectorStore(dim=embedder.dim)
    # vector_store.add(embeddings, metadata)
    #
    # # save index
    # vector_store.save(save_path)
    #
    # # save metadata
    #
    # with open(f"{save_path}/metadata.json", "w") as f:
    #     json.dump(metadata, f)
    # print(f"Saved FAISS index to {save_path}")

    build_faiss_index(chunks, metadata, embedder, save_path)
    build_bm25_index(chunks, metadata, save_path)
    print("Indexing complete (FAISS + BM25)")


# build faiss index
def build_faiss_index(chunks, metadata, embedder, save_path: str):
    embeddings = embedder.embed(chunks)  # update to embed_batch
    vector_store = VectorStore(dim=embedder.dim)
    vector_store.add(embeddings, metadata)

    # save index
    vector_store.save(save_path)

    # save metadata
    # with open(f"{save_path}/metadata.json", "w") as f:
    #     json.dump(metadata, f)
    # print(f"Saved FAISS index to {save_path}")


# build BM25 index
def build_bm25_index(chunks, metadata, save_path):
    bm25_store = BM25Store()

    # tokenized_corpus = [c.lower().split() for c in chunks]
    # bm25 = BM25Okapi(tokenized_corpus)
    # payload = {
    #     "tokenized_corpus": tokenized_corpus,
    # }
    # os.makedirs(save_path, exist_ok=True)
    #
    # with open(f"{save_path}/bm25.json", "w") as f:
    #     json.dump(payload, f)
    bm25_store.add(chunks, metadata)
    bm25_store.save(save_path)
    # print("BM25 Index saved")


def main():
    build_index(data_path="app/data/constitution.json", save_path="app/index_store")


if __name__ == "__main__":
    main()
