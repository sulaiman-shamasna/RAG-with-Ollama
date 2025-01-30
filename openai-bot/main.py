import streamlit as st
from ingestor import PdfIngestor
from footers import footer
from dotenv import load_dotenv
import os

load_dotenv()

openai_api = os.getenv('OPENAI_API_KEY')
if not openai_api:
    st.error("Error: OpenAI API key not found. Please add it to a .env file.", icon="⚠️")
    st.stop()

os.environ['OPENAI_API_KEY'] = openai_api

st.title("🦜🔗 - Chat with a PDF File")

uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")

with st.sidebar:
    st.title('💬 Chat with your Data')
    st.markdown('📖 Learn more about [LangChain](https://www.deeplearning.ai/short-courses/)')

if uploaded_file:
    file_ingestor = PdfIngestor(uploaded_file)
    file_ingestor.handlefileandingest()

st.markdown(footer, unsafe_allow_html=True)
