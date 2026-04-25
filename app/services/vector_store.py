import json
import logging
import os

import faiss
import numpy as np

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dim):
        # self.index = faiss.IndexFlatL2(dim) # euclidian distance
        self.index = faiss.IndexFlatIP(dim) # cosine similarity
        self.metadata = []

    def add(self, embeddings, metadata):
        embeddings = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_embedding, k = 5, threshold = 0.45):
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        scores, indices = self.index.search(query_embedding, k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            score = float(scores[0][i])
            # if score < threshold:
            #     continue

            meta = self.metadata[idx]
            results.append({
                "id": meta.get("id", idx),
                "answer": meta.get("chunk", ""),
                "article": meta.get("article", ""),
                "title": meta.get("title", ""),
                "category": meta.get("category", ""),
                "faiss_score": score
            })
        logger.info("vector results", results)
        return results

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # save faiss index
        faiss.write_index(self.index, f"{path}/index.faiss")

        # save metadata
        with open(f"{path}/metadata.json", "w") as f:
            json.dump(self.metadata, f)
        print("FAISS Index saved")

    def load(self, path: str):
        index_file = f"{path}/index.faiss"
        metadata_file = f"{path}/metadata.json"

        if not os.path.exists(index_file):
            raise FileNotFoundError(f"FAISS index file not found: {index_file}")

        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

        self.index = faiss.read_index(index_file)

        with open(metadata_file, "r") as f:
            self.metadata = json.load(f)

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                f"❌ Mismatch: index has {self.index.ntotal} vectors "
                f"but metadata has {len(self.metadata)} entries"
            )

        print(f"✅ Index loaded successfully")
