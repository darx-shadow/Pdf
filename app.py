import streamlit as st
import google.generativeai as genai
import pdfplumber

st.title("🤖 Gemini PDF Data Extractor")

# Setup API Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Go to Settings > Secrets and add GOOGLE_API_KEY")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # This part "reads" the file
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
        text = "\n".join(filter(None, pages)) # Cleans up empty pages
    
    if text:
        st.success(f"PDF Loaded! Found {len(text)} characters.")
        user_query = st.text_input("What data should I find?", "Summarize this.")
        
        if st.button("Extract Data"):
            with st.spinner("Gemini is working..."):
                response = model.generate_content(f"Data: {text}\n\nTask: {user_query}")
                st.write(response.text)
    else:
        st.error("We couldn't find any text in this PDF. Is it an image or scanned document?")
