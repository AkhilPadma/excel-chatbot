import pandas as pd
import streamlit as st
import requests

HF_API_KEY = st.secrets["HF_API_KEY"]
MODEL = "HuggingFaceH4/zephyr-7b-beta"

def ask_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.5, "max_new_tokens": 200},
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

    output = response.json()
    return output[0]["generated_text"] if isinstance(output, list) else output.get("generated_text")

# Streamlit UI
st.title("Excel Chatbot - Hugging Face Version")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write(df.head())

    question = st.text_input("Ask a question about your Excel data:")
    if question:
        prompt = f"Given the following dataframe:\n{df.head(10)}\n\nAnswer this: {question}"
        response = ask_huggingface(prompt)
        if response:
            st.success(response)
