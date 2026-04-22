

class HybridRetriever:
    def __init__(self, vector_store, bm25_store):
        self.vector_store = vector_store
        self.bm25_store = bm25_store

    def search(self, query, query_embedding, k = 5):
        vector_results = self.vector_store.search(query, query_embedding, k)
        bm25_results = self.bm25_store.search(query, k)

        # normalize scores
        def normalize(scores):
            min_s, max_s = min(scores), max(scores)
            return [(s - min_s) / (max_s - min_s + 1e-6) for s in scores]

        v_scores = normalize([r["score"] for r in vector_results])
        b_scores = normalize(r["bm25_Score"] for r in bm25_results)

        combined = {}

        for r, s in zip(vector_results, v_scores):
            key = r["answer"]
            combined[key] = {**r, "v_score": s, "b_score": 0}

        for r, s in zip(bm25_results, b_scores):
            key = r["answer"]
            if key in combined:
                combined[key]["b_score"] = s
            else:
                combined[key] = {**r, "v_score": 0, "b_score": s}

            # final scoring
        alpha = 0.7
        for item in combined.values():
            item["final_score"] = (
                    alpha * item["v_score"] + (1 - alpha) * item["b_score"]
            )

        # sort
        results = sorted(
            combined.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )[:k]

        return results