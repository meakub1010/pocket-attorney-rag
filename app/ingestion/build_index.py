import json

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
                    {item['article']}
                    {item['title']}
                    {item['text']}
                    """
        doc_chunks = chunker.split(text)
        for chunk in doc_chunks:
            chunks.append(chunk)
            metadata.append({
                "chunk": chunk,
                "keywords": item.get("keywords", []),
                "article": item['article'],
                "title": item['title'],
                "category": item['category'],
            })
    embeddings = embedder.embed(chunks) # update to embed_batch
    vector_store = VectorStore(dim=embedder.dim)
    vector_store.add(embeddings, metadata)

    # save index
    vector_store.save(save_path)

    # save metadata

    with open(f"{save_path}/metadata.json", "w") as f:
        json.dump(metadata, f)
    print(f"Saved index to {save_path}")


def main():
    build_index(
        data_path="app/data/constitution.json",
        save_path="app/index_store"
    )

if __name__ == "__main__":
    main()