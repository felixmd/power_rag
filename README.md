# Ragification

A modern Python application for semantic search using RAG (Retrieval-Augmented Generation) principles. This application provides a user-friendly interface for document storage and semantic search capabilities, with special support for PowerPoint presentations.

## Features

- PowerPoint presentation processing and indexing
- Document storage with metadata support
- Semantic search using FAISS and Sentence Transformers
- Modern Streamlit web interface
- SQLite database for persistent storage
- Vector similarity search

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Ragification.git
cd Ragification
```

2. Create a virtual environment and activate it:
```bash
python -m venv .rag
source .rag/bin/activate  # On Windows, use `.rag\Scripts\activate`
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

1. Place your PowerPoint files in the `resources/pptx` directory at the project root.

2. Start the Streamlit application:
```bash
cd src
streamlit run run_app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

4. Use the web interface to:
   - Load PowerPoint files from resources/pptx directory
   - Search through your documents using natural language queries
   - Add individual documents manually
   - Clear the knowledge base when needed
   - View search results with similarity scores

## Project Structure

```
Ragification/
├── src/
│   ├── ragification/
│   │   ├── api/
│   │   │   └── streamlit_app.py
│   │   ├── database/
│   │   │   └── db_manager.py
│   │   ├── embeddings/
│   │   │   └── embedding_manager.py
│   │   ├── rag_engine/
│   │   │   └── rag_manager.py
│   │   └── data_processing/
│   │       └── ppt_processor.py
│   └── run_app.py
├── resources/
│   └── pptx/           # Place your PowerPoint files here
├── requirements.txt
├── setup.py
└── README.md
```

## Dependencies

- sentence-transformers: For generating text embeddings
- faiss-cpu: For efficient similarity search
- streamlit: For the web interface
- python-pptx: For processing PowerPoint files
- numpy: For numerical operations
- setuptools: For package management

## License

MIT License 