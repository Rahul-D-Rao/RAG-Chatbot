"""
Data Loader module for RAG Chatbot using LangChain components.
"""

from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import logging
from typing import List, Dict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """
    Handles loading and preprocessing of data using LangChain components.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the DataLoader.
        
        Args:
            file_path (str): Path to the JSON file
        """
        self.file_path = file_path
        self.documents = None
        self.vectorstore = None
        
    def load_data(self) -> List[Dict]:
        """
        Load data from JSON file using LangChain's JSONLoader.
        """
        try:
            # Load JSON data
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Convert to document format
            documents = []
            for item in raw_data['data']:
                doc = {
                    'content': f"Question: {item['question']}\nAnswer: {item['answer']}",
                    'metadata': {'source': self.file_path}
                }
                documents.append(doc)
            
            self.documents = documents
            logger.info(f"Successfully loaded {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def create_vectorstore(self):
        """
        Create FAISS vectorstore using HuggingFace embeddings.
        """
        try:
            if not self.documents:
                self.load_data()
            
            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Create texts for vectorstore
            texts = [doc['content'] for doc in self.documents]
            
            # Create vectorstore
            self.vectorstore = FAISS.from_texts(texts, embeddings)
            logger.info("Successfully created vectorstore")
            
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vectorstore: {str(e)}")
            raise