import streamlit as st
import pdfplumber

st.title("Safe PDF Loader")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    # This message will show the moment the file hits the server
    st.info(f"File '{uploaded_file.name}' received by server. Analyzing...")
    
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            st.write(f"Number of pages detected: {len(pdf.pages)}")
            # Just extract first page to see if it works
            first_page_text = pdf.pages[0].extract_text()
            st.success("First page read successfully!")
            st.text(first_page_text[:500])
    except Exception as e:
        st.error(f"Upload failed at processing stage: {e}")
