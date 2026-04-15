from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed(self, texts):
        embedding = self.model.encode(texts)
        print(embedding)
        return embedding