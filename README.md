# 📘 Smart Research Assistant

An AI-powered document-aware assistant that can understand, summarize, and answer logic-based questions from uploaded research papers or PDFs. Built using **Streamlit**, **OpenAI/Ollama**, and **FAISS-based Vector Search**.

---

#Features

- Upload and process PDF or TXT files  
- Summarize the document concisely  
- Ask any question about the document  
- Generate logic-based challenge questions  
- Evaluate user answers with AI feedback  
- Optional: Use either **OpenAI** or **Ollama** backend  
- Optional: Vector search with **LangChain + FAISS**

---

#Application Architecture

 Frontend: Streamlit Web UI  
 Backend: OpenAI GPT-3.5 or Ollama Mistral (switchable)  
 Memory & Search: FAISS Vector Store + LangChain for semantic recall  
 File Parsing: `pdfplumber` and `PyPDF2` fallback  
 Session Memory: Streamlit session state  

---

#Setup & Installation

 Method 1: Google Colab (Recommended for Demo)

1. Open the project notebook in Google Colab  
2. Run all cells in order (they will:  
   - install dependencies  
   - launch the Streamlit app  
   - expose it publicly via ngrok)  
3. Upload a PDF or TXT file and interact with the assistant.

---

Method 2: Local Development

bash
```
git clone https://github.com/your-username/smart-research-assistant.git
cd smart-research-assistant

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI key (if using OpenAI)
export OPENAI_API_KEY=your-openai-key

# Run the app
streamlit run app.py
```

#Requirements
All dependencies are listed in requirements.txt.
Main packages used:
-streamlit
-openai or ollama
-angchain
-faiss-cpu
-pdfplumber, PyPDF2
-pyngrok (for Colab tunneling)

#Backend Switching

You can switch between OpenAI and Ollama in utils/llm_utils.py:
-python
-Copy
-Edit
**USE_BACKEND = os.getenv("LLM_BACKEND", "openai")
  Set the environment variable to "ollama" if using a local model like mistral.

#Use Cases
-Research document summarization
-Study & comprehension assistant
-Interactive learning & feedback
-Logic-based quiz generation

#Project Status
-Functional Requirements Implemented
-Optional Features: Vector Search, Backend Toggle
-Session memory included (Streamlit state)


