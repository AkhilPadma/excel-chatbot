import streamlit as st
import pandas as pd
import os
import requests

# Set the Streamlit page title
st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("📊 Chat with Your Excel Sheet")

# Mistral API Key Setup
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    st.warning("Please set your Mistral API token as the 'MISTRAL_API_KEY' environment variable.")
    st.stop()

MISTRAL_API_URL = "https://api.mistral.ai/v1/engines/your-engine-id/completions"
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

    # Get user input (the question they want to ask)
    user_input = st.text_input("Ask a question about your Excel data:")
    if user_input:
        # Format the prompt using the user's question and the Excel data
        prompt = f"""You are a data analyst. Here is a table:\n{df.to_markdown(index=False)}\n\nQuestion: {user_input}\nAnswer:"""

        with st.spinner("Generating response..."):
            # Send request to Mistral API
            response = requests.post(
                MISTRAL_API_URL,
                headers=HEADERS,
                json={"inputs": prompt}
            )

        # Handle response
        if response.status_code == 200:
            result = response.json()
            st.success(result.get("generated_text", "No answer generated"))
        else:
            st.error(f"Error {response.status_code} - {response.text}")
