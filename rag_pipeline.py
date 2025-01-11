"""
RAG Pipeline implementation using LangChain components.
"""

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Implements the RAG pipeline using LangChain components.
    """
    
    def __init__(self, vectorstore):
        """
        Initialize the RAG pipeline.
        
        Args:
            vectorstore: FAISS vectorstore from DataLoader
        """
        self.vectorstore = vectorstore
        self.qa_chain = None
        self.setup_chain()
        
    def setup_chain(self):
        """
        Set up the QA chain using local HuggingFace model.
        """
        try:
            # Create custom prompt template
            prompt_template = """
            Use the following pieces of context to provide a detailed and complete answer to the question below. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context: {context}
            Question: {question}
            Detailed answer:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Initialize model and tokenizer
            model_id = "google/flan-t5-small"
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            
            # Create text generation pipeline with proper parameters
            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=512,  # Increased output length
                do_sample=True,      # Enable sampling
                temperature=0.7,      # Keep temperature for creativity
                top_p=0.95,          # Add top_p sampling
                num_return_sequences=1
            )
            
            # Initialize chain with the pipeline
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=HuggingFacePipeline(pipeline=pipe),
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}  # Retrieve more context documents
                ),
                chain_type_kwargs={
                    "prompt": PROMPT,
                    "verbose": True
                }
            )
            
            logger.info("Successfully set up QA chain")
            
        except Exception as e:
            logger.error(f"Error setting up chain: {str(e)}")
            raise
            
    def get_response(self, query: str) -> str:
        """
        Get response for a query using the QA chain.
        
        Args:
            query (str): User question
            
        Returns:
            str: Generated response
        """
        try:
            # Use invoke instead of deprecated run method
            response = self.qa_chain.invoke({"query": query})
            return response['result'] if isinstance(response, dict) else response
            
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            raise