import streamlit as st

st.title("Excel Chatbot Test")
st.write("If you're seeing this, Streamlit is working!")

import pandas as pd

# App Title
st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title(" Natural Language Excel Chatbot")

# Upload section
uploaded_file = st.file_uploader(" C:\Users\akhil\excel_chatbot\sample_excel_100rows.xlsx", type=["xlsx"])

if uploaded_file:
    try:
        # Load Excel sheet into pandas
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Clean up column names: lower, replace space/specials
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


import openai
import matplotlib.pyplot as plt
import io
import contextlib

# Get API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def ask_gpt(query, df):
    schema = df.dtypes.to_dict()

    # Prompt for GPT
    prompt = f"""
You are a data analyst working with a pandas DataFrame (called `df`) with this schema:
{schema}

A user asked: "{query}"

Reply with:
1. One-liner answer (if possible)
2. Or valid Python code using pandas and matplotlib to compute the answer or show a chart.

Don't assume column names — only use what's in schema.
Return only the code (no explanation or markdown).
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response["choices"][0]["message"]["content"]

st.markdown("---")
query = st.text_input(" Ask a question about your Excel data:")

if query and uploaded_file:
    with st.spinner("Thinking..."):
        try:
            gpt_code = ask_gpt(query, df)

            st.code(gpt_code, language="python")

            # Execute code in safe env
            with contextlib.redirect_stdout(io.StringIO()) as f:
                local_env = {"df": df, "plt": plt, "st": st}
                exec(gpt_code, local_env)

            output = f.getvalue()
            if output:
                st.text(output)

        except Exception as e:
            st.error(f" Error running GPT-generated code: {e}")
