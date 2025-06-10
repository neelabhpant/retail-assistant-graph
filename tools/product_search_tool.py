# tools/product_search_tool.py
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from graph_db.driver import neo4j_driver
from sentence_transformers import SentenceTransformer
from config.config import settings

class ProductSearchInput(BaseModel):
    """Input model for the ProductSearchTool."""
    query: str = Field(description="The user's search query for a product.")

class ProductSearchTool(BaseTool):
    name: str = "Product Search Tool"
    description: str = "Searches the product catalog in the graph database to find items relevant to the user's query."
    args_schema: Type[ProductSearchInput] = ProductSearchInput
    _embedding_model: SentenceTransformer

    def __init__(self):
        super().__init__()
        self._embedding_model = SentenceTransformer(settings.embedding_model_name)

    def _run(self, query: str) -> str:
        """Executes a vector similarity search to find relevant products."""
        query_embedding = self._embedding_model.encode(query).tolist()

        with neo4j_driver.session() as session:
            # This Cypher query calls the vector index to find the most similar products
            result = session.run(
                """
                CALL db.index.vector.queryNodes('product_index', 3, $query_embedding)
                YIELD node, score
                RETURN node.name AS name, node.category AS category, node.price AS price, node.id as id, score
                """,
                query_embedding=query_embedding
            )

            products = [record for record in result]

            if not products:
                return "No relevant products found in the catalog for that query."

            # Format the output into a readable string
            response_str = "Found relevant products:\n"
            for product in products:
                if product['score'] > 0.6: # Confidence threshold
                    response_str += (
                        f"- Name: {product['name']} (ID: {product['id']})\n"
                        f"  Category: {product['category']}\n"
                        f"  Price: ${product['price']}\n\n"
                    )
            
            if response_str == "Found relevant products:\n":
                 return "No relevant products found with high enough confidence."

            return response_str