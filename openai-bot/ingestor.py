import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from streamlit_chat import message
import tempfile
import os

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA

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

        embeddings = OpenAIEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        chunks = text_splitter.split_documents(data)

        db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=DB_CHROMA_PATH
        )
        db.persist()

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            memory=memory,
        )

        def conversational_chat(query):
            result = chain({"query": query})
            st.session_state['history'].append((query, result['result']))
            return result['result']

        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! Ask me about " + self.uploaded_file.name + " 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

        response_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Enter your question, please! 💬", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
