import streamlit as st
import pandas as pd
import openai
import os

# Title
st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("🧠 Excel Chatbot using OpenAI")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Uploaded Data")
    st.dataframe(df)

    st.subheader("Column Types:")
    st.dataframe(pd.DataFrame(df.dtypes, columns=["Data Type"]).T)

    # Prompt input
    user_question = st.text_input("Ask a question about your Excel data:")

    if user_question:
        # Placeholder: Load your OpenAI API key here
        openai.api_key = os.getenv("OPENAI_API_KEY", "sk-xxxx")  # Replace with real key if available

        try:
            prompt = f"""You are an expert data analyst. Answer the following question based on this DataFrame:
            {df.head(10).to_string(index=False)}
            \n\nQuestion: {user_question}\nAnswer:"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            answer = response['choices'][0]['message']['content']
            st.markdown(f"**Answer:** {answer}")

        except Exception as e:
            st.error(f"⚠️ Unable to get a response. Reason: {str(e)}")
            st.info("Please ensure your OpenAI API key is valid and has enough quota.")
