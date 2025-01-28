import streamlit as st
from ingestor import PdfIngestor
from footers import footer
from dotenv import load_dotenv
import os

load_dotenv()

st.title("🥜🔗 - Chat with a PDF File")

uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")

if uploaded_file:
    file_ingestor = PdfIngestor(uploaded_file)
    file_ingestor.handlefileandingest()

st.markdown(footer, unsafe_allow_html=True)