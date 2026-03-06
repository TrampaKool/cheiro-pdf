import streamlit as st
from google import genai

# --- CONFIGURATION ---
# Replace with your actual API Key
API_KEY = "YOUR_GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY)

# --- UI LAYOUT ---
st.set_page_config(page_title="CheiroPDF")
st.title("Handwritten Greek to PDF")
st.write("Upload your notes, and convert them to an editable PDF.")

uploaded_files = st.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)