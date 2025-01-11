"""
Main Chatbot implementation combining DataLoader and RAGPipeline.
"""

from data_loader import DataLoader
from rag_pipeline import RAGPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Chatbot:
    """
    Main chatbot class implementing RAG-based question answering.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the chatbot.
        
        Args:
            data_path (str): Path to the input dataset
        """
        self.data_loader = DataLoader(data_path)
        self.rag_pipeline = None
        self.initialized = False
        
    def initialize(self):
        """
        Initialize components and create vectorstore.
        """
        try:
            if not self.initialized:
                # Create vectorstore
                vectorstore = self.data_loader.create_vectorstore()
                
                # Initialize RAG pipeline
                self.rag_pipeline = RAGPipeline(vectorstore)
                
                self.initialized = True
                logger.info("Chatbot initialization complete")
                
        except Exception as e:
            logger.error(f"Error initializing chatbot: {str(e)}")
            raise
            
    def get_response(self, query: str) -> str:
        """
        Get response for user query.
        
        Args:
            query (str): User question
            
        Returns:
            str: Generated response
        """
        try:
            if not self.initialized:
                self.initialize()
                
            response = self.rag_pipeline.get_response(query)
            return response
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."