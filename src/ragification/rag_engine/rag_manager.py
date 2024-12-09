from typing import List, Dict, Any
import os
import logging
from ragification.database.db_manager import DatabaseManager
from ragification.embeddings.embedding_manager import EmbeddingManager
from ragification.data_processing.ppt_processor import load_pptx_directory

# Configure logging
logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self, db_path: str = 'semantic_search.db'):
        # Get the data directory path
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")
        
        # Initialize managers with proper paths
        self.db_path = os.path.join(self.data_dir, db_path)
        self.index_path = os.path.join(self.data_dir, 'faiss.index')
        logger.info(f"Using database path: {self.db_path}")
        logger.info(f"Using index path: {self.index_path}")
        
        self.db_manager = DatabaseManager(self.db_path)
        self.embedding_manager = EmbeddingManager(index_path=self.index_path)
    
    def add_document(self, original_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        """Add a document to both database and vector store"""
        try:
            # Generate embedding
            embedding = self.embedding_manager.generate_embedding(content)
            logger.debug(f"Generated embedding for document: {original_id}")
            
            # Add to FAISS index
            vector_id = self.embedding_manager.add_to_index(embedding)
            logger.debug(f"Added embedding to index with vector_id: {vector_id}")
            
            # Add to database
            success = self.db_manager.add_document(original_id, content, metadata, vector_id)
            if success:
                logger.info(f"Successfully added document: {original_id}")
            else:
                logger.warning(f"Failed to add document: {original_id}")
            return success
        except Exception as e:
            logger.error(f"Error adding document {original_id}: {str(e)}")
            return False
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            logger.info(f"Searching for query: {query} with k={k}")
            
            # Generate query embedding
            query_embedding = self.embedding_manager.generate_embedding(query)
            logger.debug("Generated query embedding")
            
            # Search in FAISS
            distances, indices = self.embedding_manager.search_similar(query_embedding, k)
            logger.debug(f"Found indices: {indices}, distances: {distances}")
            
            # Retrieve documents
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx == -1:  # Skip invalid indices
                    continue
                doc = self.db_manager.get_document_by_vector_id(int(idx))
                if doc:
                    doc['similarity_score'] = float(1 / (1 + distance))
                    results.append(doc)
            
            logger.info(f"Found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []
    
    def load_pptx_files(self, directory_path: str = 'resources/pptx') -> int:
        """Load all PPTX files from the specified directory"""
        try:
            # Get the project root directory (two levels up from this file)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            ppt_dir = os.path.join(project_root, directory_path)
            logger.info(f"Loading PPT files from: {ppt_dir}")
            
            documents = load_pptx_directory(ppt_dir)
            logger.info(f"Found {len(documents)} slides in PPT files")
            
            success_count = 0
            for doc in documents:
                if self.add_document(doc['original_id'], doc['content'], doc['metadata']):
                    success_count += 1
            
            logger.info(f"Successfully loaded {success_count} slides")
            return success_count
        except Exception as e:
            logger.error(f"Error loading PPT files: {str(e)}")
            return 0
    
    def clear_knowledge_base(self) -> None:
        """Clear all documents from the database and reset the vector store"""
        try:
            self.db_manager.clear_documents()
            self.embedding_manager.clear_index()
            logger.info("Successfully cleared knowledge base")
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {str(e)}")