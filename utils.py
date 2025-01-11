"""
Utility functions for the RAG chatbot application.
"""

import logging
from typing import List, Dict
from fpdf import FPDF
import textwrap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_chat_history(chat_history: List[Dict[str, str]], filename: str):
    """
    Save chat history to a PDF file.
    
    Args:
        chat_history (List[Dict[str, str]]): List of chat messages
        filename (str): Output filename (should end with .pdf)
    """
    try:
        # Create PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Set margins
        pdf.set_left_margin(20)
        pdf.set_right_margin(20)
        
        # Add title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Chat History", ln=True, align='C')
        pdf.ln(10)
        
        # Reset font for content
        pdf.set_font("Arial", size=12)
        
        # Process chat history
        for i in range(0, len(chat_history), 2):
            if i + 1 < len(chat_history):
                # Get question and answer
                question = chat_history[i]['text']
                answer = chat_history[i + 1]['text']
                
                # Add question
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "Question:", ln=True)
                pdf.set_font("Arial", size=12)
                
                # Wrap text to fit page width
                wrapped_question = textwrap.fill(question, width=80)
                for line in wrapped_question.split('\n'):
                    pdf.cell(0, 10, line, ln=True)
                pdf.ln(5)
                
                # Add answer
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "Response by Chatbot:", ln=True)
                pdf.set_font("Arial", size=12)
                
                # Wrap text to fit page width
                wrapped_answer = textwrap.fill(answer, width=80)
                for line in wrapped_answer.split('\n'):
                    pdf.cell(0, 10, line, ln=True)
                pdf.ln(10)
        
        # Save PDF
        pdf_filename = filename if filename.endswith('.pdf') else f"{filename}.pdf"
        pdf.output(pdf_filename)
        logger.info(f"Chat history saved to {pdf_filename}")
        
    except Exception as e:
        logger.error(f"Error saving chat history: {str(e)}")

def format_message(message: str, is_user: bool = True) -> str:
    """
    Format a chat message with appropriate prefix.
    
    Args:
        message (str): Message content
        is_user (bool): Whether the message is from the user
        
    Returns:
        str: Formatted message
    """
    prefix = "Question: " if is_user else "Response by Chatbot: "
    return f"{prefix}{message}"

def validate_question(question: str) -> bool:
    """
    Validate if a question is properly formatted.
    
    Args:
        question (str): Question to validate
        
    Returns:
        bool: True if question is valid, False otherwise
    """
    question = question.strip()
    if not question:
        return False
    if len(question) < 3:
        return False
    return True