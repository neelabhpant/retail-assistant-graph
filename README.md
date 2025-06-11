# 🛍️ AI Retail Assistant (Graph Edition)

This project is an advanced, AI-powered retail assistant built on a multi-agent framework (CrewAI) and a powerful Neo4j graph database backend. It is designed to intelligently understand and respond to complex customer queries by leveraging graph-based data relationships and Retrieval-Augmented Generation (RAG).

The core of this system is its ability to perform sophisticated tasks like personalized product recommendations through collaborative filtering, which is made possible by the Neo4j graph architecture.

## 💡 System in Action

### Interactive User Interface (Streamlit)
The application provides a clean, conversational UI for users to interact with the AI assistant.
![Screenshot 2025-06-11 at 10 32 08 AM](https://github.com/user-attachments/assets/a8dd9d23-688f-4c12-93c2-0b2324ffe596)



### The Knowledge Graph (Neo4j)
All data, including customers, products, and orders, is stored as an interconnected graph, allowing the system to understand complex relationships.
![Screenshot 2025-06-10 at 9 12 50 PM](https://github.com/user-attachments/assets/1bf021bc-52db-42db-9315-a0dd38fcc5eb)

![Screenshot 2025-06-10 at 9 13 25 PM](https://github.com/user-attachments/assets/28f0a2b4-d74f-41d6-8d51-bfe700257485)


## ✨ Core Features

* **Graph-Powered Backend:** All data is stored and queried from a Neo4j database.
* **Advanced Recommendation Engine:** Uses collaborative filtering on the graph to provide personalized "customers who bought this also bought..." suggestions.
* **Multi-Agent System (CrewAI):** Orchestrates a team of specialized AI agents for robust and modular task handling.
* **Hybrid Search (RAG):** Performs semantic vector search for FAQs and products directly within Neo4j.
* **Specialized Tools:** A full suite of tools for retrieving order history, processing returns, and generating recommendations.
* **Persistent Knowledge:** Uses Docker for running the Neo4j database, ensuring data persistence.

## 🛠️ Tech Stack

* **AI Framework:** CrewAI
* **LLM Provider:** OpenAI (GPT-4o)
* **Graph Database:** Neo4j (run via Docker)
* **Vector Search:** Neo4j Vector Index
* **Embedding Model:** Sentence Transformers
* **Web UI:** Streamlit
* **Language:** Python 3.12

## ⚙️ Setup and Installation

### Prerequisites

* Python 3.10+
* Docker Desktop
* An OpenAI API Key

### Quick Start Guide

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/neelabhpant/retail-assistant-graph.git](https://github.com/neelabhpant/retail-assistant-graph.git)
    cd retail-assistant-graph
    ```

2.  **Set Up Environment & Install Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    * Create a `.env` file in the project root.
    * Add your credentials:
        ```env
        OPENAI_API_KEY="your_api_key_here"
        NEO4J_URI="bolt://localhost:7687"
        NEO4J_USERNAME="neo4j"
        NEO4J_PASSWORD="password123"
        OPENAI_MODEL_NAME="gpt-4o"
        ```

4.  **Launch Neo4j using Docker:**
    ```bash
    docker run -d --name neo4j-retail-db -p 7474:7474 -p 7687:7687 -v neo4j_retail_data:/data -e NEO4J_AUTH=neo4j/password123 neo4j:latest
    ```

5.  **Ingest Data into Neo4j:**
    ```bash
    python -m graph_db.ingest_data
    ```

## ▶️ How to Run the Application

1.  Ensure your virtual environment is active and the Neo4j Docker container is running.
2.  From the project root, launch the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```
