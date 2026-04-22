import json
import os

from rank_bm25 import BM25Okapi

class BM25Store:
    def __init__(self):
        self.tokenized_corpus = []
        self.metadata = []
        self.bm25 = None

    def add(self, documents, metadata):
        self.tokenized_corpus = [doc.split() for doc in documents]
        self.metadata.extend(metadata)
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, query, k=5):
        print("BM25 search")
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:k]

        results = []
        for idx in top_indices:
            results.append({
                "id": idx,
                "answer": self.metadata[idx].get("chunk", ""),
                "article": self.metadata[idx].get("article", ""),
                "title": self.metadata[idx].get("title", ""),
                "category": self.metadata[idx].get("category", ""),
                "bm25_score": scores[idx]
            })

        return results

    def save(self, save_path):
        os.makedirs(save_path, exist_ok=True)

        payload = {
            "tokenized_corpus": self.tokenized_corpus,
            "metadata": self.metadata,
        }
        with open(f"{save_path}/bm25.json", "w") as f:
            json.dump(payload, f)
        print("BM25 index saved")

    def load(self, save_path):
        file = f"{save_path}/bm25.json"

        if not os.path.exists(file):
            raise FileNotFoundError(f"BM25 file {file} does not exist")

        with open(file, "r") as f:
            data = json.load(f)
        self.tokenized_corpus = data["tokenized_corpus"]
        self.metadata = data["metadata"]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

        print("BM25 index loaded")