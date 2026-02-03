import streamlit as st
import pdfplumber
import google.generativeai as genai

st.set_page_config(page_title="PDF AI")
st.title("🚀 Smart PDF Processor")

# 1. Setup API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing Key in Secrets!")
    st.stop()

# 2. Upload Area
uploaded_file = st.file_uploader("Drop PDF here", type=["pdf"])

# 3. Processing Trigger
if uploaded_file:
    st.info(f"File selected: {uploaded_file.name}")
    
    # We use a button to FORCE the code to start reading
    if st.button("Read PDF Now"):
        try:
            with st.spinner("Reading contents..."):
                with pdfplumber.open(uploaded_file) as pdf:
                    text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            
            if text:
                st.success("Read successful!")
                # Send to Gemini
                response = model.generate_content(f"Summarize this: {text}")
                st.subheader("Results:")
                st.write(response.text)
            else:
                st.warning("Found the file, but it looks empty or scanned.")
        except Exception as e:
            st.error(f"Error: {e}")
