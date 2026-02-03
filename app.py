import streamlit as st
import pdfplumber
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI PDF Extractor", layout="centered")
st.title("🤖 Gemini PDF Assistant")

# 2. Setup the "Brain" (Gemini)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key! Please add GOOGLE_API_KEY to your Streamlit Secrets.")
    st.stop()

# 3. Flexible File Uploader 
# (Removed the type filter so you can actually see your files)
uploaded_file = st.file_uploader("Upload your file below")

if uploaded_file is not None:
    # Check if the file is actually a PDF
    if not uploaded_file.name.lower().endswith(".pdf"):
        st.error(f"Please upload a PDF. You selected: {uploaded_file.name}")
    else:
        st.success(f"File Caught: {uploaded_file.name}")
        
        # 4. User Question
        user_query = st.text_input("What data should I extract?", "Summarize this document.")

        # 5. Manual Trigger Button
        if st.button("Process PDF with AI"):
            try:
                with st.spinner("Reading PDF..."):
                    # Open and extract text
                    with pdfplumber.open(uploaded_file) as pdf:
                        full_text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                full_text += page_text + "\n"
                
                if full_text.strip():
                    with st.spinner("Gemini is thinking..."):
                        # Send text to Gemini
                        prompt = f"Using this PDF text:\n{full_text}\n\nTask: {user_query}"
                        response = model.generate_content(prompt)
                        
                        st.subheader("Results:")
                        st.markdown(response.text)
                else:
                    st.warning("The PDF was read, but no text was found. It might be a scan/image.")
            
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Footer instructions
st.markdown("---")
st.caption("Tip: If you don't see your PDF, change the 'File Type' dropdown in your file picker to 'All Files'.")
