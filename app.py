import streamlit as st
import pdfplumber
import google.generativeai as genai

st.title("Final Debug Test")

# STEP 1: Check Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Secrets are missing!")
    st.stop()

# STEP 2: File Uploader
# If this doesn't show up, your requirements.txt is wrong
file = st.file_uploader("Upload PDF here", type="pdf")

if file is not None:
    st.write(f"File detected: {file.name}")
    
    try:
        # STEP 3: Try to open the PDF
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        if text:
            st.success("✅ Success! Text found.")
            st.text_area("Preview of text:", text[:500]) # Show first 500 characters
            
            # STEP 4: Ask Gemini
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if st.button("Ask Gemini"):
                res = model.generate_content(f"Summarize: {text}")
                st.write(res.text)
        else:
            st.warning("⚠️ The file uploaded, but no text was found inside it.")
            
    except Exception as e:
        st.error(f"The code crashed here: {e}")
