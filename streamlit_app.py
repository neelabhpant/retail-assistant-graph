# streamlit_app.py
import streamlit as st
import sys
import os

sys.path.append(os.getcwd())

from crew.crew_setup import RetailCrew
from graph_db.driver import Neo4jDriver
from config.config import settings

def main():
    st.set_page_config(page_title="AI Retail Assistant", layout="wide")

    st.title("🛍️ AI Retail Assistant (Graph Edition)")
    st.markdown(f"**Model:** `{settings.openai_model_name}` | **Database:** `Neo4j`")

    st.sidebar.header("About")
    st.sidebar.info(
        "This AI-powered retail assistant uses a multi-agent system (CrewAI) "
        "and a Neo4j Graph Database to provide intelligent, context-aware answers."
    )
    st.sidebar.header("Enter Customer ID")
    customer_id = st.sidebar.text_input("Customer ID", value="C001")

    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome! How can I help you today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about products, your orders, or our policies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Our AI team is on the case... Please wait."):
                full_prompt = f"I am customer {customer_id}. {prompt}"

                retail_crew = RetailCrew(full_prompt)
                result = retail_crew.run()

                st.markdown(result)

        st.session_state.messages.append({"role": "assistant", "content": result})

if __name__ == "__main__":
    try:
        main()
    finally:
        Neo4jDriver.close_driver()