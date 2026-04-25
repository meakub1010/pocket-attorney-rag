import logging

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, vector_store, bm25_store, embedder):
        self.vector_store = vector_store
        self.bm25_store = bm25_store
        self.embedder = embedder

    def retrieve(self, query, k = 10):
        q_embedding = self.embedder.embed([query])
        vector_results = self.vector_store.search(q_embedding, k)

        bm25_results = self.bm25_store.search(query, k)

        print("length: ", len(vector_results), len(bm25_results))

        print("Vector results: \n", vector_results)
        print("BM25 results: \n", bm25_results)

        # Fallback safety
        if not vector_results:
            return bm25_results, q_embedding
        if not bm25_results:
            return vector_results, q_embedding
        combined = {}
        alpha = 0.5

        # normalize scores
        def normalize(scores):
            scores = list(scores)  # ensure list

            if not scores:
                return []

            min_s, max_s = min(scores), max(scores)

            if max_s == min_s:
                return [1.0] * len(scores)

            return [(s - min_s) / (max_s - min_s + 1e-6) for s in scores]

        v_scores = normalize([r["faiss_score"] for r in vector_results])
        b_scores = normalize([r["bm25_score"] for r in bm25_results])

        # -------------------
        # Add vector results
        # -------------------
        for r, s in zip(vector_results, v_scores):
            key = r["id"]
            combined[key] = {**r, "v_score": s, "b_score": 0}

        # -------------------
        # Add BM25 results
        # -------------------
        for r, s in zip(bm25_results, b_scores):
            key = r["id"]

            if key in combined:
                combined[key]["b_score"] = s
            else:
                combined[key] = {**r, "v_score": 0, "b_score": s}

        # -------------------
        # Final scoring
        # -------------------
        for item in combined.values():
            item["final_score"] = (
                    alpha * item["v_score"] +
                    (1 - alpha) * item["b_score"]
            )

        # sort + top k
        results = sorted(
            combined.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )[:8]

        print(f"hybrid retriever: \n\n", results)

        # set to cache
        # await self.cache.set(q_embedding, results)
        return results, q_embedding

