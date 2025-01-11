"""
Streamlit application for the CS Knowledge Hub - An intelligent assistant for Computer Science and AI topics.
"""

import streamlit as st
import os
from datetime import datetime
from chatbot import Chatbot
from utils import save_chat_history, validate_question

# Ensure the output directory exists
os.makedirs('outputs', exist_ok=True)

# Page configuration
st.set_page_config(
    page_title="CS Knowledge Hub | Your AI & Computer Science Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput > div > div > input {
        background-color: black !important;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2e7d32;
        color: white;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #1976d2;
        color: white;
        align-self: flex-start;
    }
    .similar-question {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chatbot' not in st.session_state:
    try:
        st.session_state.chatbot = Chatbot('Input_Dataset.json')
        st.session_state.chatbot.initialize()
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        st.stop()

# Sidebar
st.sidebar.title("🎓 CS Knowledge Hub")
st.sidebar.markdown("---")

# About section in sidebar
st.sidebar.markdown("""
### About
CS Knowledge Hub is your intelligent assistant for all things Computer Science! Get answers about:

- 🤖 Artificial Intelligence
- 💻 Programming Languages
- 🔐 Cybersecurity
- 🌐 Web Development
- 📊 Data Structures & Algorithms
- 🗄️ Databases
- 🔧 Software Engineering
- ⚙️ Operating Systems
- 🔍 Computer Architecture
- 🧮 Theory of Computation

### Features
- Instant answers to CS questions
- Local RAG-based processing
- Exportable chat history (PDF)
- Reliable knowledge base
""")

# Export functionality
if st.sidebar.button("Export Chat History (PDF)"):
    if st.session_state.chat_history:
        filename = f"outputs/chat_history.pdf"
        save_chat_history(st.session_state.chat_history, filename)
        st.sidebar.success(f"Chat history exported to {filename}")
    else:
        st.sidebar.warning("No chat history to export!")

# Clear chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.sidebar.success("Chat history cleared!")

# Main chat interface
st.title("🎓 Your CS & AI Knowledge Assistant")
st.markdown("Ask me anything about Computer Science, Programming, AI, and related topics!")

# Display chat history
for message in st.session_state.chat_history:
    if message["is_user"]:
        st.markdown(
            f"""<div class="chat-message user-message">
                <div><strong>You:</strong> {message["text"]}</div>
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div class="chat-message bot-message">
                <div><strong>Assistant:</strong> {message["text"]}</div>
            </div>""",
            unsafe_allow_html=True
        )

# Input form
with st.form(key='query_form', clear_on_submit=True):
    user_query = st.text_input("Type your question here:", key="user_query")
    submit_button = st.form_submit_button("Ask")

    if submit_button and user_query:
        if validate_question(user_query):
            try:
                # Add user message to chat history
                st.session_state.chat_history.append({
                    "text": user_query,
                    "is_user": True
                })

                # Get response
                response = st.session_state.chatbot.get_response(user_query)

                # Add bot response to chat history
                st.session_state.chat_history.append({
                    "text": response,
                    "is_user": False
                })

                # Rerun to update the display
                st.rerun()
            except Exception as e:
                st.error("An error occurred while processing your question. Please try again.")
        else:
            st.warning("Please enter a valid question (at least 3 characters).")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit and LangChain",
    unsafe_allow_html=True
)
