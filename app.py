import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.markdown("""
<style>
/* Global font size */
html, body, [class*="css"]  {
    font-size: 18px !important;  /* Change this as needed */
}

/* Title */
h1 {
    font-size: 2.5em !important;
}

/* Sidebar */
.css-1d391kg, .css-1v3fvcr {
    font-size: 1.2em !important;
}

/* Chat messages */
.stChatMessage, .stMarkdown, .stTextInput {
    font-size: 1.2em !important;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
POSTGRES = "USE_POSTGRES"

radio_opt = [ "Connect to your PostgreSQL Database"]

selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

db_uri = None
postgresql_host = None
postgresql_user = None
postgresql_password = None
postgresql_db = None

if radio_opt.index(selected_opt) == 0:
    db_uri = POSTGRES
    postgresql_host = st.sidebar.text_input("Provide PostgreSQL Host")
    postgresql_user = st.sidebar.text_input("PostgreSQL User")
    postgresql_password = st.sidebar.text_input("PostgreSQL password", type="password")
    postgresql_db = st.sidebar.text_input("PostgreSQL database", value="demodb")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input(label="GROQ API Key", type="password")

if not db_uri:
    st.info("Please choose a database option.")
    st.stop()

if not api_key:
    st.info("Please add the GROQ API key")
    st.stop()


@st.cache_resource
def get_llm():
    """Initializes and caches the LLM."""
    return ChatGroq(groq_api_key=st.secrets.groq_api_key, model_name="Llama3-8b-8192", streaming=True)



# Updated configure_db function
@st.cache_resource(ttl="2h")
def configure_db(db_uri):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == POSTGRES:
        # Connect using st.secrets
        try:
            return SQLDatabase(create_engine(
                f"postgresql+psycopg2://{st.secrets.connections.postgresql.username}:{st.secrets.connections.postgresql.password}@{st.secrets.connections.postgresql.host}:{st.secrets.connections.postgresql.port}/{st.secrets.connections.postgresql.database}"
            ))
        except ImportError:
            st.error("Psycopg2 library not found. Please install it with: `pip install psycopg2-binary`")
            st.stop()
        except Exception as e:
            st.error(f"Failed to connect to PostgreSQL: {e}")
            st.stop()


if db_uri == POSTGRES:
    db = configure_db(db_uri, pg_host=postgresql_host, pg_user=postgresql_user, pg_password=postgresql_password, pg_db=postgresql_db)
else:
    db = configure_db(db_uri)

## toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=get_llm(api_key))

agent = create_sql_agent(
    llm=get_llm(api_key),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.write(response)
