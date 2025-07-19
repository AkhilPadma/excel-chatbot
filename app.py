import streamlit as st
import pandas as pd
import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")  # Set this in Streamlit Cloud or locally

# Streamlit UI
st.title("📊 Excel Chatbot with Hugging Face Inference API")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📁 Data Preview")
    st.dataframe(df)

    user_question = st.text_input("Ask a question about your Excel data:")

    if user_question:
        context = df.to_csv(index=False)
        prompt = f"""You are an assistant. Use the following data table to answer the question.\n\nData:\n{context}\n\nQuestion: {user_question}"""

        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200}
        }

        with st.spinner("Thinking..."):
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()[0]["generated_text"]
                st.subheader("🧠 Response")
                st.write(result)
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
