from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Union, List, Tuple
import faiss
import os

class EmbeddingManager:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_path: str = 'faiss.index'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index_path = index_path
        self.index = self._load_or_create_index()
    
    def _load_or_create_index(self) -> faiss.Index:
        """Load existing FAISS index or create a new one"""
        if os.path.exists(self.index_path):
            try:
                return faiss.read_index(self.index_path)
            except Exception as e:
                print(f"Error loading index: {e}. Creating new index.")
        
        # Create a new index with L2 normalization
        index = faiss.IndexFlatL2(self.dimension)
        return index
    
    def _save_index(self) -> None:
        """Save the FAISS index to disk"""
        try:
            faiss.write_index(self.index, self.index_path)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def generate_embedding(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for a text or list of texts"""
        embeddings = self.model.encode(text, convert_to_numpy=True)
        # Ensure the embeddings are normalized
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        faiss.normalize_L2(embeddings)
        return embeddings
    
    def add_to_index(self, embedding: np.ndarray) -> int:
        """Add an embedding to the FAISS index and return its ID"""
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        
        # Ensure the embedding is normalized
        faiss.normalize_L2(embedding)
        
        self.index.add(embedding)
        self._save_index()
        return self.index.ntotal - 1
    
    def search_similar(self, query_embedding: np.ndarray, k: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar embeddings in the index"""
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Ensure the query embedding is normalized
        faiss.normalize_L2(query_embedding)
        
        # If index is empty, return empty results
        if self.index.ntotal == 0:
            return np.array([[0] * k]), np.array([[-1] * k])
        
        return self.index.search(query_embedding, min(k, self.index.ntotal))
    
    def clear_index(self) -> None:
        """Clear the FAISS index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        if os.path.exists(self.index_path):
            try:
                os.remove(self.index_path)
            except Exception as e:
                print(f"Error removing index file: {e}")
        self._save_index()