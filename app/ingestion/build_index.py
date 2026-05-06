import json
import os

from pinecone import Pinecone, ServerlessSpec
from rank_bm25 import BM25Okapi

from app.services.bm25_store import BM25Store
from app.services.chunking.factory import get_chunker
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStore

# run this script using below command
# uv run python -m app.ingestion.build_index
# script has been registered as project.scripts in toml


from dotenv import load_dotenv

load_dotenv()


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


# build BM25 index
def build_bm25_index(chunks, metadata, save_path):
    bm25_store = BM25Store()
    bm25_store.add(chunks, metadata)
    bm25_store.save(save_path)


def get_or_create_index(name: str, dim:int):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    existing = [i.name for i in pc.list_indexes()]
    if name not in existing:
        pc.create_index(
            name=name,
            dimension=dim,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(name)


def build_pinecone_index(index_name: str, data_path: str):
    embedder = EmbeddingService()
    kb_index = get_or_create_index(index_name, embedder.dim)
    chunker = get_chunker()

    with open(data_path) as f:
        data = json.load(f)

    vectors = []

    for item in data:
        text = f"""
                       {item["article"]}
                       {item["title"]}
                       {item["text"]}
                       """
        doc_chunks = chunker.split(text)
        for i, chunk in enumerate(doc_chunks):
            vector_id = f"{item["article"].lower().replace(' ', '_')}_chunk_{i}"
            vectors.append({
                "id": vector_id,
                "values": embedder.embed(chunk),
                "metadata": {
                    "chunk": chunk,
                    "keywords": item.get("keywords", []),
                    "article": item["article"],
                    "title": item["title"],
                    "category": item["category"],
                },
            })
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        kb_index.upsert(vectors=vectors[i : i + batch_size])

    print(f"Upserted {len(vectors)} vectors to '{index_name}'")


def main():
    # build_index(data_path="app/data/constitution.json", save_path="app/index_store")
    build_pinecone_index(index_name="kb-index", data_path="app/data/constitution.json")


if __name__ == "__main__":
    main()
