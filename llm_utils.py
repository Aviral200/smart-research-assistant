import os
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

USE_BACKEND = os.getenv("LLM_BACKEND", "openai")  # or "ollama"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if USE_BACKEND == "openai":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    import ollama

def ask_llm(prompt: str) -> str:
    if USE_BACKEND == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    else:
        resp = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return "".join(chunk["message"]["content"] for chunk in resp)

# Vector DB
def build_vector_db(text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(text)]
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    return db

def query_vector_db(db, query: str):
    docs = db.similarity_search(query, k=1)
    return docs[0].page_content if docs else "(No relevant snippet found)"

def summarize_document(text: str) -> str:
    prompt = f"Summarize this document in 150 words:\n\n{text[:4000]}"
    return ask_llm(prompt)

def answer_question(text: str, question: str) -> str:
    snippet = query_vector_db(build_vector_db(text), question)
    prompt = f"Answer this question based on the following:\n\n{snippet}\n\nQ: {question}\nA:"
    return ask_llm(prompt)

def generate_logic_questions(text: str, n=3) -> list:
    prompt = f"Generate {n} logic-based questions from the text:\n\n{text[:4000]}"
    return [q.strip("-* ") for q in ask_llm(prompt).splitlines() if q.strip()][:n]

def evaluate_user_answer(text: str, question: str, user_answer: str) -> str:
    snippet = query_vector_db(build_vector_db(text), question)
    prompt = f"Evaluate this answer based on the following:\n\n{snippet}\n\nQ: {question}\nUser: {user_answer}\nFeedback:"
    return ask_llm(prompt)
