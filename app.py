import streamlit as st
import google.generativeai as genai
import pdfplumber

# Setup the Page
st.title("🤖 Gemini PDF Data Extractor")
st.write("Upload a PDF and ask me to find specific data!")

# Connect to Gemini (we will add the key in the settings later)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key! Please add it in the App Settings.")

# Upload File
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "".join([page.extract_text() for page in pdf.pages])

    st.success("PDF Uploaded!")
    user_query = st.text_input("What data should I extract?", "List the items and their prices.")

    if st.button("Generate"):
        with st.spinner("Thinking..."):
            response = model.generate_content(f"Text: {text}\n\nTask: {user_query}")
            st.markdown(response.text)
