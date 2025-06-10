# 🛍️ AI Retail Assistant (Graph Edition)

This project is an advanced, AI-powered retail assistant built on a multi-agent framework (CrewAI) and a powerful Neo4j graph database backend. It is designed to intelligently understand and respond to complex customer queries by leveraging graph-based data relationships and Retrieval-Augmented Generation (RAG).

The core of this system is its ability to perform sophisticated tasks like personalized product recommendations through collaborative filtering, which is made possible by the Neo4j graph architecture.

## ✨ Core Features

* **Graph-Powered Backend:** All data, including customers, products, orders, and their relationships, is stored and queried from a Neo4j database.
* **Advanced Recommendation Engine:** A new `RecommendationTool` uses collaborative filtering on the graph to provide personalized "customers who bought this also bought..." suggestions.
* **Multi-Agent System (CrewAI):** Orchestrates a team of specialized AI agents (Query Router, Retail Assistant, Summarizer) for robust and modular task handling.
* **Hybrid Search (RAG):**
    * Performs semantic vector search for FAQs and products directly within Neo4j.
    * Combines traditional structured queries with AI-powered vector search.
* **Specialized Tools:** A full suite of tools for retrieving order history, processing returns, searching products, answering FAQs, and generating recommendations.
* **Conversational UI (Streamlit):** An interactive chat interface for a seamless user experience.
* **Persistent & Scalable:** Uses Docker for running the Neo4j database, ensuring data persistence and a clean environment.

## 🛠️ Tech Stack

* **AI Framework:** CrewAI
* **LLM Provider:** OpenAI (GPT-4o or configurable)
* **Graph Database:** Neo4j (run via Docker)
* **Vector Search:** Neo4j Vector Index
* **Embedding Model:** Sentence Transformers
* **Web UI:** Streamlit
* **Language:** Python 3.12

## 🧠 Architecture Overview

1.  **User Interface (Streamlit):** Captures user input.
2.  **CrewAI Pipeline:**
    * **Query Router Agent:** Decomposes complex user queries into distinct intents.
    * **Retail Assistant Agent:** Executes tasks by selecting the appropriate tool from its suite to query the Neo4j database.
    * **Summarizer Agent:** Synthesizes the factual data retrieved by the tools into a single, cohesive, customer-facing response.
3.  **Data Layer (Neo4j):**
    * A single, unified database stores all nodes (Customers, Products, Orders, FAQs) and their relationships (e.g., `PLACED`, `CONTAINS`).
    * Vector embeddings for products and FAQs are stored directly on the nodes, enabling powerful hybrid searches.

## ⚙️ Setup and Installation

### Prerequisites

* Python 3.10+
* Docker Desktop
* An OpenAI API Key

### Quick Start Guide

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/neelabhpant/retail-assistant-graph.git](https://github.com/neelabhpant/retail-assistant-graph.git)
    cd retail-assistant-graph
    ```

2.  **Set Up Virtual Environment & Install Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    * Create a `.env` file in the project root.
    * Add your credentials and settings:
        ```env
        OPENAI_API_KEY="your_api_key_here"
        NEO4J_URI="bolt://localhost:7687"
        NEO4J_USERNAME="neo4j"
        NEO4J_PASSWORD="password123"
        OPENAI_MODEL_NAME="gpt-4o"
        ```

4.  **Launch Neo4j using Docker:**
    * Ensure Docker Desktop is running.
    * Use the following command to start a persistent Neo4j instance:
        ```bash
        docker run -d --name neo4j-retail-db -p 7474:7474 -p 7687:7687 -v neo4j_retail_data:/data -e NEO4J_AUTH=neo4j/password123 neo4j:latest
        ```

5.  **Ingest Data into Neo4j:**
    * Before running for the first time, you need to populate your graph database.
    * Run the ingestion script from the project root:
        ```bash
        python -m graph_db.ingest_data
        ```

## ▶️ How to Run the Application

1.  Ensure your virtual environment is active and the Neo4j Docker container is running.
2.  From the project root, launch the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```
    The application will open in your browser, ready for you to interact with.

---
