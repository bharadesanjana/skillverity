import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, index_path="data/vector_index.faiss", meta_path="data/vector_meta.pkl", dimension=384):
        self.index_path = index_path
        self.meta_path = meta_path
        self.dimension = dimension
        self.index = None
        self.metadata = []
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def save_index(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def add_texts(self, texts, metas, embeddings):
        """
        texts: list of strings
        metas: list of dicts
        embeddings: numpy array of shape (n, dimension)
        """
        if len(texts) == 0:
            return
        
        self.index.add(embeddings)
        self.metadata.extend(metas)
        self.save_index()

    def search(self, query_embedding, k=5):
        """
        query_embedding: numpy array of shape (1, dimension)
        """
        D, I = self.index.search(query_embedding, k)
        results = []
        for i, idx in enumerate(I[0]):
            if idx < len(self.metadata) and idx != -1:
                results.append({
                    "metadata": self.metadata[idx],
                    "score": float(D[0][i])
                })
        return results

# Singleton instance
vector_store = VectorStore()
