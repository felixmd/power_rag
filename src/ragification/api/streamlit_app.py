import streamlit as st
from ragification.rag_engine.rag_manager import RAGManager
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Ragification - Semantic Search")
    
    # Initialize RAG manager
    rag_manager = RAGManager()
    
    # Sidebar for database operations
    st.sidebar.header("Knowledge Base Operations")
    
    # Load PPT files
    if st.sidebar.button("Load PPT Files"):
        with st.spinner("Loading PPT files from resources/pptx..."):
            count = rag_manager.load_pptx_files()
            logger.info(f"Loaded {count} slides from PPT files")
            if count > 0:
                st.sidebar.success(f"Successfully loaded {count} slides!")
            else:
                st.sidebar.warning("No slides were loaded. Make sure PPT files exist in resources/pptx directory.")
    
    # Clear knowledge base
    if st.sidebar.button("Clear Knowledge Base"):
        confirm = st.sidebar.warning("Are you sure? This will delete all documents!")
        if confirm:
            rag_manager.clear_knowledge_base()
            st.sidebar.success("Knowledge base cleared successfully!")
            logger.info("Knowledge base cleared")
    
    # Search interface
    st.header("Search Documents")
    query = st.text_input("Enter your search query:")
    k = st.slider("Number of results", min_value=1, max_value=10, value=3)
    
    if st.button("Search"):
        if query:
            with st.spinner("Searching..."):
                logger.info(f"Searching for: {query}")
                results = rag_manager.search(query, k)
                logger.info(f"Found {len(results)} results")
                logger.info(f"Search results: {json.dumps(results, indent=2)}")
                
                if results:
                    st.success(f"Found {len(results)} relevant documents!")
                    for i, result in enumerate(results, 1):
                        with st.container():
                            st.subheader(f"Result {i}")
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown("**Content:**")
                                st.write(result['content'])
                                st.markdown("**Document ID:**")
                                st.write(result['original_id'])
                            
                            with col2:
                                st.markdown("**Similarity Score:**")
                                st.write(f"{result['similarity_score']:.2f}")
                                with st.expander("Metadata"):
                                    st.json(result['metadata'])
                            
                            st.divider()
                else:
                    st.warning("No results found.")
                    logger.warning("No results found for query: " + query)
        else:
            st.warning("Please enter a search query.")

    # Document upload interface
    st.header("Add New Document")
    content = st.text_area("Document Content:")
    original_id = st.text_input("Document ID:")
    metadata = st.text_area("Metadata (JSON format):", "{}")
    
    if st.button("Add Document"):
        if content and original_id:
            try:
                metadata_dict = json.loads(metadata)
                logger.info(f"Adding document with ID: {original_id}")
                if rag_manager.add_document(original_id, content, metadata_dict):
                    st.success("Document added successfully!")
                    logger.info("Document added successfully")
                else:
                    st.error("Failed to add document. ID might already exist.")
                    logger.error(f"Failed to add document with ID: {original_id}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format in metadata.")
                logger.error("Invalid JSON format in metadata")
        else:
            st.warning("Please fill in both content and document ID.")

if __name__ == "__main__":
    main() 