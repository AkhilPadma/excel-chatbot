import streamlit as st
import pandas as pd
import os
import requests

# Set the Streamlit page title
st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title(" Chat with Your Excel Sheet")

# Mistral API Key Setup
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    st.warning("Please set your Mistral API token as the 'MISTRAL_API_KEY' environment variable.")
    st.stop()

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Preview of your data:")
    st.dataframe(df)

    # Get user input
    user_input = st.text_input("Ask a question about your Excel data:")
    if user_input:
        try:
            # Convert DataFrame to markdown format
            table_md = df.to_markdown(index=False)
        except ImportError:
            st.error("Missing 'tabulate' package required for to_markdown(). Please add it to your requirements.txt")
            st.stop()

        # Prompt formatting
        prompt = f"""You are a helpful data analyst. Here is the Excel data table:\n{table_md}\n\nQuestion: {user_input}\nAnswer:"""

        with st.spinner("Generating response from Mistral..."):
            response = requests.post(
                MISTRAL_API_URL,
                headers=HEADERS,
                json={
                    "model": "mistral-tiny",  # Use mistral-small or mistral-medium if available to you
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                }
            )

        if response.status_code == 200:
            result = response.json()
            st.success(result["choices"][0]["message"]["content"])
        else:
            st.error(f"Error {response.status_code} - {response.text}")
