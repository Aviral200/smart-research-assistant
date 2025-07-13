import streamlit as st
import re
from utils.pdf_parser import extract_text_from_pdf
from utils.llm_utils import (
    summarize_document,
    answer_question,
    generate_logic_questions,
    evaluate_user_answer
)

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📘 Smart Research Assistant")

for key in ['document_text', 'summary', 'qa_history',
            'challenge_questions', 'challenge_user_answers',
            'challenge_feedback', 'current_file']:
    if key not in st.session_state:
        st.session_state[key] = None if 'history' not in key and 'answers' not in key else []

uploaded_file = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
if uploaded_file:
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.update({
            'summary': None,
            'qa_history': [],
            'challenge_questions': [],
            'challenge_user_answers': [],
            'challenge_feedback': [],
            'current_file': uploaded_file.name
        })
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    st.session_state['document_text'] = text
    if not st.session_state['summary']:
        with st.spinner("Summarizing document..."):
            st.session_state['summary'] = summarize_document(text)
    st.subheader("Auto Summary")
    st.info(st.session_state['summary'])

if st.session_state.get("document_text"):
    tab1, tab2 = st.tabs(["💬 Ask Anything", "🧠 Challenge Me"])
    with tab1:
        question = st.text_input("Your Question:")
        if st.button("Get Answer"):
            answer = answer_question(st.session_state["document_text"], question)
            snippet = re.search(r'"([^"]{20,300})"', answer)
            st.session_state["qa_history"].append({
                "q": question, "a": answer, "snippet": snippet.group(1) if snippet else ""
            })
        for entry in reversed(st.session_state["qa_history"]):
            st.markdown(f"**Q:** {entry['q']}")
            st.markdown(f"**A:** {entry['a']}")
            if entry["snippet"]:
                st.markdown(f"> 📌 *Evidence:* {entry['snippet']}")
            st.markdown("---")

    with tab2:
        if not st.session_state["challenge_questions"]:
            if st.button("Generate Questions"):
                st.session_state["challenge_questions"] = generate_logic_questions(st.session_state["document_text"])
                st.session_state["challenge_user_answers"] = [""] * len(st.session_state["challenge_questions"])
        for i, q in enumerate(st.session_state["challenge_questions"]):
            st.markdown(f"**Q{i+1}:** {q}")
            st.session_state["challenge_user_answers"][i] = st.text_area(
                f"Your answer to Q{i+1}:", key=f"ans{i}", value=st.session_state["challenge_user_answers"][i]
            )
        if st.button("Submit Answers"):
            feedbacks = []
            for i, q in enumerate(st.session_state["challenge_questions"]):
                fb = evaluate_user_answer(st.session_state["document_text"], q, st.session_state["challenge_user_answers"][i])
                feedbacks.append(fb)
            st.session_state["challenge_feedback"] = feedbacks
        if st.session_state.get("challenge_feedback"):
            st.subheader("Challenge Feedback")
            for i, fb in enumerate(st.session_state["challenge_feedback"]):
                st.markdown(f"**Q{i+1} Feedback:** {fb}")
else:
    st.info("📄 Upload a PDF or TXT document to begin.")
