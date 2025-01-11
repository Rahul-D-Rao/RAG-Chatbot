"""
Utility functions for the RAG chatbot application.
"""

import logging
from typing import List, Dict
from fpdf import FPDF
import textwrap
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_chat_history_to_memory(chat_history):
    """
    Save chat history to a PDF in memory.

    Args:
        chat_history (list): List of chat messages.

    Returns:
        BytesIO: In-memory PDF data.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(200, 10, txt="Chat History", ln=True, align="C")
    pdf.ln(10)

    # Chat content
    pdf.set_font("Arial", size=12)
    for message in chat_history:
        if message["is_user"]:
            pdf.set_text_color(0, 0, 255)  # Blue for user messages
            pdf.multi_cell(0, 10, f"User: {message['text']}")
        else:
            pdf.set_text_color(0, 128, 0)  # Green for bot messages
            pdf.multi_cell(0, 10, f"Assistant: {message['text']}")
        pdf.ln(5)

    # Write PDF content to a BytesIO stream
    pdf_data = BytesIO()
    pdf_string = pdf.output(dest="S").encode("latin1")  # Output PDF as string and encode it
    pdf_data.write(pdf_string)
    pdf_data.seek(0)  # Reset stream pointer to the beginning

    return pdf_data

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
