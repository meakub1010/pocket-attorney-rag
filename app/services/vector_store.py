import faiss
import numpy as np

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

    def search(self, query_embedding, k = 5, threshold = 0.20):
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        scores, indices = self.index.search(query_embedding, k)
        print("scores: ", scores[:1])
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            score = float(scores[0][i])
            if score < threshold:
                continue

            meta = self.metadata[idx]
            results.append({
                "answer": meta.get("chunk", ""),
                "article": meta.get("article", ""),
                "title": meta.get("title", ""),
                "category": meta.get("category", ""),
                "score": score
            })
        return results