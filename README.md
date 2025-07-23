# 📊 Excel Chatbot using Mistral AI 🚀

Interact with your Excel sheets using natural language! Upload any `.xlsx` file and ask data-related questions like:

> "What is the average salary by department?"  
> "How many employees are full-time?"  
> "Show the total number of males and females."

This Streamlit app uses the **Mistral AI API (`mistral-tiny`)** to generate insights by embedding your Excel data into a prompt.

---

## 🔧 Features

- 📁 Upload Excel files (`.xlsx`, `.xls`)
- 💬 Ask questions in natural language
- 🤖 Uses [Mistral AI](https://docs.mistral.ai/api/) for LLM responses
- 📊 Data preview table (via `pandas`)
- 🧠 Converts DataFrame to markdown for structured prompting

---

## 🧱 Tech Stack

| Layer        | Technology            |
|--------------|------------------------|
| Frontend     | Streamlit              |
| Backend      | Python, Pandas         |
| LLM API      | Mistral (`mistral-tiny`) |
| Deployment   | Streamlit Cloud / GitHub |

---

## 📸 Screenshots

### 🖼️ Upload & Preview
![Upload](
<img width="1450" height="816" alt="image" src="https://github.com/user-attachments/assets/0a1b92aa-46ce-432c-8602-d19340cd3633" />
<img width="1239" height="696" alt="image" src="https://github.com/user-attachments/assets/709698c4-836a-4efb-b7bb-02b508d43dcd" />
)

WEB APP : https://excel-chatbot-6qrb8bqhbbkg5gbu5u4ysn.streamlit.app/

## 🚀 Getting Started (Local)

> You don’t need to run locally if using GitHub + Streamlit Cloud. But here’s how if you want to:

git clone https://github.com/your-username/excel-chatbot
cd excel-chatbot

# Create virtual env
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt

# Set your Mistral API Key
export MISTRAL_API_KEY="your-api-key-here"  # or use .env file

# Run the app
streamlit run app.py


