import logging

logger = logging.getLogger(__name__)


class HybridRetriever:
    def __init__(self, vector_store, bm25_store):
        self.vector_store = vector_store
        self.bm25_store = bm25_store

    async def retrieve(self, question, q_embedding, k=10):
        vector_results = self.vector_store.search(q_embedding, k)

        bm25_results = self.bm25_store.search(question, k)
        vector_results = [
            r
            for r in vector_results
            if r.get("faiss_score") is not None and r["faiss_score"] > 0.3
        ]  # tune: 0.25 - 0.4

        # Fallback safety
        if not vector_results:
            return bm25_results[:3]
        if not bm25_results:
            return vector_results[:3]
        combined = {}

        alpha = 0.7  # favor FAISS

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
                alpha * item["v_score"] + (1 - alpha) * item["b_score"]
            )

        all_items = list(combined.values())

        if not all_items:
            return []

        # -------------------
        # Step 7: Threshold filtering (MOST IMPORTANT)
        # -------------------
        max_score = max(item["final_score"] for item in all_items)

        # Dynamic threshold (key improvement)
        threshold = max_score * 0.6  # tune: 0.5–0.7

        filtered = [item for item in all_items if item["final_score"] >= threshold]

        # -------------------
        # Step 8: Fallback safety
        # -------------------
        if len(filtered) < 2:
            filtered = sorted(all_items, key=lambda x: x["final_score"], reverse=True)[
                :2
            ]

        # -------------------
        # Step 9: Final Top-K (small context for LLM)
        # -------------------
        results = sorted(filtered, key=lambda x: x["final_score"], reverse=True)[:3]
        return results
