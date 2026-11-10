# PlacidWay Website Knowledge Chatbot

An AI-powered RAG (Retrieval-Augmented Generation) chatbot built for the PlacidWay AI Automation Engineer Assessment. The bot answers visitor questions strictly using approved PlacidWay knowledge base pages, with strict anti-hallucination guardrails and source citation.

---

## 🛠️ Tech Stack & Tools
- **Language & Framework:** Python, Streamlit (for instant UI & public deployment)
- **RAG Orchestration:** LangChain
- **Vector Database:** ChromaDB (in-memory/local)
- **Embeddings & LLM:** OpenAI Embeddings & `gpt-4o-mini`
- **Web Scraping:** BeautifulSoup & `WebBaseLoader` with custom User-Agent

---

## 🚀 Setup & Local Execution Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GOUF97/placidway-chatbot-assessment.git
   cd placidway-chatbot-assessment
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

4. **Enter your OpenAI API Key** in the sidebar UI input field to initialize the knowledge base and start testing.

---

## 🏛️ Architecture Overview
1. **Content Ingestion:** Scrapes the 7 approved PlacidWay URLs respecting polite crawler headers and rate limits.
2. **Chunking & Storage:** Splits text into manageable 1000-character chunks with 200-character overlap, embedding them into a Chroma vector store.
3. **Retrieval & Strict Grounding:** Uses semantic search to fetch relevant context passages, passing them to `gpt-4o-mini` with a rigorous system prompt enforcing strict source grounding and "I don't know" fallback behaviors.
