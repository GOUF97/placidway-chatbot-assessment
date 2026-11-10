import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Page Config
st.set_page_config(
    page_title="PlacidWay Medical Tourism AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("PlacidWay Knowledge & Cost Assistant")
st.markdown("Ask questions about ITC Immunity Therapy Center treatments, pricing, packages, and comparisons based strictly on official PlacidWay data.")

# Sidebar for API Key & Data Refresh
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Enter OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    
    st.markdown("---")
    st.header("Knowledge Base")
    st.info("The bot loads content dynamically from the 7 approved PlacidWay URLs.")
    
    if st.button("Refresh Knowledge Base"):
        st.cache_resource.clear()
        st.success("Knowledge base cache cleared and reloaded!")

if not api_key_input:
    st.warning("Please enter your OpenAI API Key in the sidebar to start chatting.")
    st.stop()

# Approved URLs
URLS = [
    "https://www.placidway.com/clinic/1801/ITC-Immunity-Therapy-Center-Alternative-Cancer-Treatment",
    "https://www.placidway.com/treatment-package/36737/Alternative-Adenocarcinoma-Cancer-Treatment-in-Tijuana",
    "https://www.placidway.com/treatment-package/36738/Alternative-Adrenal-Cancer-Treatment-in-Tijuana",
    "https://www.placidway.com/treatment-package/36739/Alternative-Anal-Cancer-Treatment-in-Tijuana",
    "https://www.placidway.com/videos/1801/ITC-Tijuana-Videos-Alternative-Cancer-Treatment",
    "https://www.placidway.com/price/1801/ITC-Immunity-Therapy-Center-Price-List",
    "https://www.placidway.com/comparison-price/Alternative-Medicine-Cost-Abroad-Compare-Prices-2026"
]

@st.cache_resource
def get_vector_store(api_key):
    # Load documents with custom user agent
    loader = WebBaseLoader(URLS)
    loader.requests_kwargs = {'headers': {'User-Agent': 'PlacidWayBot/1.0 (Medical Tourism QA Crawler)'}}
    docs = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embeddings & Vector Store
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})

try:
    retriever = get_vector_store(api_key_input)
except Exception as e:
    st.error(f"Error loading knowledge base: {e}")
    st.stop()

# LLM & Prompt Setup
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key_input)

system_prompt = (
    "You are an expert AI Assistant for PlacidWay, a global medical tourism platform. "
    "Your task is to answer user questions strictly based on the provided context retrieved from official PlacidWay pages. "
    "CRITICAL RULES:\n"
    "1. ACCURACY & GROUNDING: Answer ONLY using facts, prices, treatments, and clinics present in the context. Every answer must cite its source URL(s).\n"
    "2. HONEST 'I DON'T KNOW': If the exact answer, price, or clinic is not present in the context, you MUST state: 'I do not have that information in my knowledge base.' and suggest contacting PlacidWay for a free quote. Never invent prices, clinics, or medical facts.\n"
    "3. COST QUESTIONS: Return prices with exact currency and any context given in the page (e.g., 'starting from', package inclusions).\n"
    "4. TRICK & OUT OF SCOPE: Reject wrong assumptions (e.g., false prices), politely decline out-of-scope questions (weather, general trivia), and refuse to give direct medical diagnoses or safety advice for specific health conditions, recommending consultation with a doctor instead.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Chat Messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# User Input
if user_query := st.chat_input("Ask a question about treatments, costs, or clinics..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("assistant"):
        with st.spinner("Searching PlacidWay knowledge base..."):
            try:
                response = rag_chain.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.chat_history
                })
                answer = response["answer"]
                
                # Extract source URLs if available in retrieved docs
                sources = set()
                if "context" in response:
                    for doc in response["context"]:
                        if "source" in doc.metadata:
                            sources.add(doc.metadata["source"])
                
                if sources:
                    answer += "\n\n**Sources:**\n" + "\n".join([f"- [{src}]({src})" for src in sources])
                
                st.markdown(answer)
                st.session_state.chat_history.append(AIMessage(content=answer))
            except Exception as e:
                err_msg = f"An error occurred: {str(e)}"
                st.error(err_msg)
