import streamlit as st
import pandas as pd
import openai
import os
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Excel Chatbot", layout="wide")

# API Key (set it via Streamlit secrets or environment)
api_key = os.getenv("OPENAI_API_KEY", "sk-xxxx")  # Replace or use secrets
client = OpenAI(api_key=api_key)

# Title
st.title(" Excel Chatbot using OpenAI API")

# Upload file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Preview of Excel Data")
    st.dataframe(df)

    st.subheader("Column Types:")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column'}))

    st.subheader("Ask a question about your Excel data:")
    question = st.text_input("")

    if question:
        # Construct prompt
        prompt = f"""
        You are a data assistant. The following is a pandas DataFrame:
        {df.head(10).to_markdown()}
        
        Answer this question based on the DataFrame:
        {question}
        
        Return Python code to answer this.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            code = response.choices[0].message.content.strip("`python").strip("`").strip()

            st.subheader(" Generated Code:")
            st.code(code, language="python")

            try:
                # Execute the generated code safely
                local_env = {"df": df}
                exec(code, {}, local_env)
                output = local_env.get("output", "No output variable returned.")
                st.subheader(" Result:")
                st.write(output)
            except Exception as e:
                st.error(f"Error executing generated code: {e}")

        except Exception as e:
            st.error(f"API Error: {e}")
