import streamlit as st
import google.generativeai as genai
import pdfplumber

st.set_page_config(page_title="PDF Extractor")
st.title("📄 PDF Data Extractor")

# 1. API Key Check
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ API Key not found! Go to Streamlit Settings > Secrets and add: GOOGLE_API_KEY = 'your_key'")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. File Uploader
uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

if uploaded_file is not None:
    try:
        # 3. Extract Text
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    all_text += extracted + "\n"
        
        if not all_text.strip():
            st.warning("⚠️ This PDF seems to be an image (scanned). I can't read text from images yet.")
        else:
            st.success("✅ PDF text extracted successfully!")
            
            # 4. User Question
            user_task = st.text_input("What should I find in this PDF?", "Summarize the key points")
            
            if st.button("Generate Result"):
                with st.spinner("Gemini is reading..."):
                    prompt = f"Here is the text from a PDF:\n\n{all_text}\n\nTask: {user_task}"
                    response = model.generate_content(prompt)
                    st.markdown("### 🤖 Analysis:")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"❌ Error processing PDF: {e}")
