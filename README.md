# CS Knowledge Hub - RAG-based Chatbot 🎓

A locally-running intelligent assistant for Computer Science topics using Retrieval-Augmented Generation (RAG) with LangChain and Streamlit.

## 🌟 Features

- **Local RAG Processing**: Uses FAISS for efficient vector storage and retrieval
- **Interactive UI**: Clean and responsive Streamlit interface
- **Topic Coverage**:
  - Artificial Intelligence & Machine Learning
  - Programming Languages
  - Data Structures & Algorithms
  - Web Development
  - Cybersecurity
  - Databases
  - Software Engineering
  - Operating Systems
  - Computer Architecture
  - Theory of Computation
- **Export Functionality**: Save chat history to PDF
- **Local Model**: Uses HuggingFace's flan-t5-small model for inference

## 📋 Prerequisites

- Python 3.9+
- pip (Python package manager)
- 4GB+ RAM recommended
- CUDA-compatible GPU (optional, for faster inference)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Rahul-D-Rao/RAG-Chatbot.git
cd RAGChatbot
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Prepare your knowledge base JSON file:
```json
{
    "data": [
        {
            "question": "What is artificial intelligence?",
            "answer": "Artificial intelligence is the simulation of human intelligence processes by machines, especially computer systems."
        },
        ...
    ]
}
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

## 📁 Project Structure

```
RAGChatbot/
├── app.py              # Streamlit web application
├── chatbot.py          # Main chatbot implementation
├── data_loader.py      # Data loading and vectorstore creation
├── rag_pipeline.py     # RAG implementation using LangChain
├── utils.py            # Utility functions
├── requirements.txt    # Project dependencies
├── outputs/
│    └──chat_history.pdf       # Directory for exported chat histories
└──__pycache__/
   ├──chatbot.cpython-312.pyc
   ├──data_loader.cpython-312.pyc
   ├──rag_pipeline.cpython-312.pyc
   └──utils.cpython-312.pyc
```

## 🔧 Configuration

The application uses several key components that can be configured:

- **Embeddings Model**: Currently uses `sentence-transformers/all-MiniLM-L6-v2`
- **LLM Model**: Uses `google/flan-t5-small`
- **Vector Store**: FAISS for efficient similarity search
- **Chat History**: Automatically saved and can be exported to PDF

## 📥 Input Dataset Format

The input dataset should be a JSON file with the following structure:
```json
{
    "data": [
        {
            "question": "Question text",
            "answer": "Answer"
        }
    ]
}
```

## 🛟 Troubleshooting

Common issues and solutions:

1. **ModuleNotFoundError**: 
   - Ensure you've installed all dependencies: `pip install -r requirements.txt`
   - Make sure you're in the virtual environment

2. **CUDA/GPU Issues**:
   - The application runs on CPU by default
   - For GPU support, install appropriate CUDA toolkit and PyTorch version

3. **Memory Issues**:
   - Reduce the size of your input dataset
   - Use a smaller model
   - Reduce the number of retrieved documents in RAG pipeline

## 🔍 Dependencies

Main dependencies include:
- `streamlit`: Web interface
- `langchain`: RAG implementation
- `transformers`: Machine learning models
- `sentence-transformers`: Text embeddings
- `faiss-cpu`: Vector storage (or `faiss-gpu` for GPU support)
- `fpdf`: PDF export functionality

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request

## ✨ Future Improvements

- [ ] Add support for larger models
- [ ] Implement streaming responses
- [ ] Add source citations to answers
- [ ] Improve context retrieval with re-ranking
- [ ] Add chat history persistence
- [ ] Implement user authentication
- [ ] Add support for code execution
- [ ] Improve answer quality with better prompting
