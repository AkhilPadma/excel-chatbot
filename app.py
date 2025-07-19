import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import contextlib
from langchain_community.llms import HuggingFaceHub
import os

# App Title
st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title(" Natural Language Excel Chatbot")

# Set Hugging Face API Token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# Upload section
uploaded_file = st.file_uploader(" Upload an Excel (.xlsx) file", type=["xlsx"])

if uploaded_file:
    try:
        # Load Excel sheet into pandas
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Clean up column names
        df.columns = [
            col.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("$", "")
            for col in df.columns
        ]

        # Show success and preview
        st.success(" File uploaded and data loaded successfully!")
        st.write(" First few rows of your data:")
        st.dataframe(df.head())

        # Show info about the schema
        st.write(" Column Types:")
        st.write(df.dtypes)

    except Exception as e:
        st.error(f" Error reading the Excel file: {e}")
else:
    st.info(" Please upload an Excel file to continue.")

def ask_model(query, df):
    """
    Asks a question to a locally run language model.
    """
    schema = df.dtypes.to_dict()

    prompt = f"""
You are a data analyst working with a pandas DataFrame called `df` with this schema:
{schema}

A user asked: "{query}"

Reply with valid Python code using pandas and matplotlib to compute or visualize the answer.
Use only column names from the schema above.
Don't explain the code, just return the Python code directly.
"""
    
    # Initialize the Hugging Face model
    llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature":0.1, "max_length":512})
    
    response = llm(prompt)

    return response

st.markdown("---")
query = st.text_input(" Ask a question about your Excel data:")

if query and uploaded_file:
    with st.spinner("Thinking..."):
        try:
            model_code = ask_model(query, df)

            # Ensure the response is treated as code
            st.code(model_code, language="python")

            # Execute code in a safe environment
            with contextlib.redirect_stdout(io.StringIO()) as f:
                local_env = {"df": df, "plt": plt, "st": st}
                exec(model_code, local_env)

            output = f.getvalue()
            if output:
                st.text(output)

        except Exception as e:
            st.error(f" Error running the generated code: {e}")