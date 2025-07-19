import streamlit as st
import pandas as pd
from transformers import pipeline
import tempfile

# Load model pipeline once
@st.cache_resource
def load_pipeline():
    return pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")

qa_pipeline = load_pipeline()

# Streamlit UI
st.title("📊 Excel Chatbot using Hugging Face (Offline)")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Read Excel into DataFrame
    df = pd.read_excel(uploaded_file)
    st.subheader("🔍 Preview of Your Data")
    st.dataframe(df)

    # Ask a question
    question = st.text_input("Ask a question about your Excel data:")
    
    if question:
        with st.spinner("Thinking..."):
            # Convert df to CSV as a prompt context
            csv_context = df.to_csv(index=False)
            prompt = f"""You are a helpful assistant. Given this table data:\n{csv_context}\n\nAnswer this question based on the data: {question}"""
            
            result = qa_pipeline(prompt, max_new_tokens=200, do_sample=True)[0]['generated_text']
            
            st.subheader("🧠 Response")
            st.write(result)
