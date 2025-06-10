# tools/faq_tool.py
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from graph_db.driver import neo4j_driver
from sentence_transformers import SentenceTransformer
from config.config import settings

class FAQInput(BaseModel):
    """Input model for the FAQTool."""
    query: str = Field(description="The user's question about a specific topic.")

class FAQTool(BaseTool):
    name: str = "FAQ Search Tool"
    description: str = "Searches the FAQ knowledge base in the graph database to find answers to user questions."
    args_schema: Type[BaseModel] = FAQInput
    _embedding_model: SentenceTransformer

    def __init__(self):
        super().__init__()
        self._embedding_model = SentenceTransformer(settings.embedding_model_name)

    def _run(self, query: str) -> str:
        """Executes a vector similarity search query in Neo4j."""
        query_embedding = self._embedding_model.encode(query).tolist()

        with neo4j_driver.session() as session:
            # This Cypher query calls the vector index to find the most similar FAQ
            result = session.run(
                """
                CALL db.index.vector.queryNodes('faq_index', 1, $query_embedding)
                YIELD node, score
                RETURN node.text AS text, score
                """,
                query_embedding=query_embedding
            ).single()

            if result and result["score"] > 0.7: # Confidence threshold
                return f"Relevant FAQ found (Similarity Score: {result['score']:.2f}):\n{result['text']}"
            else:
                return "No relevant information found in the FAQ database for that question."