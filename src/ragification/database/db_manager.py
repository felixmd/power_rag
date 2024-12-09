import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional
import os

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_database()
    
    def _create_database(self) -> None:
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_id TEXT UNIQUE,
                content TEXT,
                metadata JSON,
                vector_id INTEGER UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            conn.commit()
    
    def add_document(self, original_id: str, content: str, metadata: Dict[str, Any], vector_id: int) -> bool:
        """Add a new document to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO documents (original_id, content, metadata, vector_id)
                VALUES (?, ?, ?, ?)
                ''', (original_id, content, json.dumps(metadata), vector_id))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_document_by_vector_id(self, vector_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a document by its vector ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT content, metadata, original_id 
            FROM documents 
            WHERE vector_id = ?
            ''', (vector_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'content': row[0],
                    'metadata': json.loads(row[1]),
                    'original_id': row[2]
                }
            return None
    
    def clear_documents(self) -> None:
        """Clear all documents from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM documents')
            conn.commit() 

