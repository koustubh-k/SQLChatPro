# 🦜 SQLChatPro — Chat with Your SQL Database using LangChain + Groq

An interactive Streamlit application to **chat with your PostgreSQL database** using **LangChain** and **Groq's ultra-fast LLMs**. Easily connect to your database, ask natural language questions, and receive insights — all in real-time!

![SQLChatPro Screenshot](screenshot.png)

---

## 🚀 Features

- 🧠 Natural language querying on PostgreSQL databases
- 🔌 Easy connection to your own database (via sidebar inputs)
- ⚡ Fast responses using Groq Llama3-8B model
- 💬 Chat interface with history tracking
- 🔒 Secure handling of credentials via Streamlit sidebar
- 🖼️ Customizable UI (larger fonts, themed chat)

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — for UI
- [LangChain](https://www.langchain.com/) — agent and tool logic
- [Groq API](https://console.groq.com/) — LLM backend
- [SQLAlchemy](https://www.sqlalchemy.org/) — database abstraction
- [psycopg2](https://pypi.org/project/psycopg2-binary/) — PostgreSQL connector

---

## 🧑‍💻 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/sqlchatpro.git
cd sqlchatpro

pip install -r requirements.txt

streamlit run app.py

```
🔐 API & Database Setup
Get a Groq API Key

Prepare your PostgreSQL database

Ensure it's accessible from your machine

Note down host, user, password, and database name
