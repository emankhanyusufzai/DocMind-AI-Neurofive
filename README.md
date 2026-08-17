# DocMind AI 🧠

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **grounded only in the content of an uploaded document** — built for the Neurofive Solutions internship (Week 3: Generative AI & Prompt Engineering).

Instead of relying on the LLM's memory (which can hallucinate), DocMind AI retrieves the most relevant chunks from your document and generates answers strictly from that context — with sources cited for every response.

---

## ✨ Features

- 📄 Upload any PDF and chat with its content
- 🔍 Semantic search over document chunks using FAISS vector store
- 🤖 Grounded answers powered by Google Gemini (`gemini-2.5-flash`)
- 🧩 Local embeddings via HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- 📌 Source page numbers shown for every answer, for easy verification
- 🎨 Clean, dark-themed Streamlit chat interface

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Orchestration | LangChain |
| Vector Store | FAISS (local) |
| Embeddings | HuggingFace (`all-MiniLM-L6-v2`) |
| LLM | Google Gemini (`gemini-2.5-flash`) |
| PDF Parsing | pypdf |

---

## 🌐 Live Demo

Try it here: [DocMind AI — Live App](https://docmind-ai-neurofive-2gklnukaajqecscprky5fx.streamlit.app/)

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/emankhanyusufzai/DocMind-AI-Neurofive.git
   cd DocMind-AI-Neurofive
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser, upload a PDF, click **Ingest Document**, and start asking questions.

---

## 🧪 Grounding vs. Plain Prompting

This project was tested by asking the model 5+ questions that required reading the actual document content (specific numbers, named stages, exact test results). With RAG grounding enabled, all answers matched the source document exactly, with correct page citations and no hallucinated content — compared to a plain prompt (no retrieval), which would rely purely on the model's training data and could not answer document-specific details like exact test scores or custom terminology at all.

---

## 📎 Project Context

Built as part of the **Neurofive Solutions Internship — Week 3, Generative AI & Prompt Engineering** module (RAG Mini-Project: "Chat With Your Own Document").

## 📄 Project Documentation

Full write-up: [Project Documentation](https://docs.google.com/document/d/1HtPXWvscS5GE7-Dfh2FgeRClIGc2Vows/edit?usp=sharing&ouid=113277923944516120692&rtpof=true&sd=true)

## 🎥 Demo Video

Watch the demo on LinkedIn: [DocMind AI — Demo Video](https://www.linkedin.com/posts/eman-khan-903603339_generativeai-rag-langchain-ugcPost-7495185102428143616-3Ubt/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFT8MVMBerQm95j5Cxvue7ggwSGs-Rvjalg)