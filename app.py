import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="DocMind AI", page_icon="🧠", layout="wide")

# ---------- Session state ----------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (question, answer, sources)

# ---------- Cached resources ----------
@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGoogleGenerativeAI(
        google_api_key=GEMINI_API_KEY,
        model="gemini-2.5-flash",
        temperature=0.2,
    )

PROMPT = ChatPromptTemplate.from_template(
    """You are DocMind AI, an assistant that answers questions using ONLY the
context provided below, which was retrieved from the user's uploaded document.
If the answer is not contained in the context, say clearly that the document
does not contain that information — do not guess or use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""
)

def build_vectorstore(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore, len(chunks)

def answer_question(question: str):
    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 4})
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in retrieved_docs)

    llm = get_llm()
    chain = PROMPT | llm
    response = chain.invoke({"context": context, "question": question})

    sources = [f"Page {d.metadata.get('page', '?')}" for d in retrieved_docs]
    return response.content, sources

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧠 DocMind AI")
    st.caption("Chat with your own document — powered by RAG")
    st.divider()

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("📥 Ingest Document", use_container_width=True):
            with st.spinner("Reading, chunking, and embedding document..."):
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                vs, num_chunks = build_vectorstore(temp_path)
                st.session_state.vectorstore = vs
                st.session_state.chat_history = []
            st.success(f"Ingested! {num_chunks} chunks indexed.")

    st.divider()
    st.markdown("### 📊 Knowledge Base")
    if st.session_state.vectorstore is not None:
        st.success("Document loaded ✅")
    else:
        st.info("No document loaded yet.")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ---------- Main area ----------
st.title("🧠 DocMind AI")
st.caption("Ask questions about your uploaded document. Answers are grounded only in its content.")

if st.session_state.vectorstore is None:
    st.warning("👈 Upload and ingest a PDF from the sidebar to get started.")
else:
    question = st.chat_input("Ask a question about your document...")

    if question:
        with st.spinner("Thinking..."):
            answer, sources = answer_question(question)
            st.session_state.chat_history.append((question, answer, sources))

    for q, a, sources in reversed(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)
            st.caption(f"Sources: {', '.join(sources)}")

st.divider()
st.caption("Built for Neurofive Solutions Internship — Week 3: RAG Mini-Project")