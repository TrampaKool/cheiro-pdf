import streamlit as st
from google import genai
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- UI LAYOUT ---
st.set_page_config(page_title="CheiroPDF")
st.title("Handwritten Greek to PDF")
st.write("Upload your notes, and convert them to an editable PDF.")

if not API_KEY:
    st.error("API Key not found! Check your .env file.")
    st.stop()

uploaded_files = st.file_uploader(
    "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if uploaded_files:
    print(API_KEY);
    st.info(f"Loaded {len(uploaded_files)} images.")
    
    if st.button("Start Transcription"):
        all_text = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            # Update UI
            percent = (i + 1) / len(uploaded_files)
            progress_bar.progress(percent)
            status_text.text(f"Processing image {i+1} of {len(uploaded_files)}...")

            # Convert uploaded file to bytes for the API
            img_bytes = file.read()
            
            # Call Gemini API
            try:
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview",
                    contents=[
                        "Transcribe this handwritten Greek text.",
                        {"inline_data": {"data": img_bytes, "mime_type": "image/jpeg"}}
                    ]
                )
                all_text.append(response.text)
            except Exception as e:
                st.error(f"Error on page {i+1}: {e}")
            
            # Throttling to stay in Free Tier (approx 10 requests per minute)
            time.sleep(6)

        status_text.success("All images processed!")
        print(f"Server-side: {all_text}")