import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from ollama_utils import OllamaLLM
import tempfile
import os

from dotenv import load_dotenv
import os

load_dotenv()

openai_api = os.getenv('OPENAI_API_KEY')
if not openai_api:
    st.error("Error: OpenAI API key not found. Please add it to a .env file.", icon="⚠️")
    st.stop()

os.environ['OPENAI_API_KEY'] = openai_api

DB_CHROMA_PATH = '/vectorstore/db1'

class PdfIngestor:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def handlefileandingest(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            loader = PyMuPDFLoader(file_path=tmp_file_path)
            data = loader.load()
        finally:
            os.remove(tmp_file_path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(data)

        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=DB_CHROMA_PATH)
        db.persist()

        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        llm = OllamaLLM(model_name="llama3.2")

        def conversational_chat(query):
            retrieved_docs = retriever.get_relevant_documents(query)
            context = " ".join([doc.page_content for doc in retrieved_docs])
            prompt = f"Context: {context}\n\nQuestion: {query}"
            response = llm.chat(prompt)
            return response.get("content", "Error: No response from model")

        st.session_state['history'] = []

        response_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Ask your question! 💬", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['history'].append((user_input, output))

        with response_container:
            for i, (user_msg, bot_reply) in enumerate(st.session_state['history']):
                st.write(f"**You:** {user_msg}")
                st.write(f"**Bot:** {bot_reply}")