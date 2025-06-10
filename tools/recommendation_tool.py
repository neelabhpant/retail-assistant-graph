# tools/recommendation_tool.py
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from graph_db.driver import neo4j_driver

class RecommendationInput(BaseModel):
    """Input model for the RecommendationTool."""
    customer_id: str = Field(description="The unique identifier of the customer for whom to generate recommendations.")

class RecommendationTool(BaseTool):
    name: str = "Personalized Product Recommendation Tool"
    description: str = (
        "Generates personalized product recommendations for a customer based on the purchasing behavior of similar customers. "
        "Use this when a user asks for suggestions, ideas, what they might like, or what they should buy next."
    )
    args_schema: Type[RecommendationInput] = RecommendationInput

    def _run(self, customer_id: str) -> str:
        """Executes a collaborative filtering query in Neo4j to generate recommendations."""
        with neo4j_driver.session() as session:
            # This Cypher query implements a collaborative filtering recommendation strategy.
            # Find products the target customer has already bought.
            # Find other customers who also bought at least one of those same products.
            # Find what *other* products those similar customers bought.
            # Filter out products the target customer has already purchased.
            # Count the occurrences of each recommended product and return the top 5.
            result = session.run(
                """
                MATCH (c:Customer {id: $customer_id})-[:PLACED]->(:Order)-[:CONTAINS]->(p:Product)
                WITH c, COLLECT(p) AS purchased_products
                
                MATCH (other:Customer)-[:PLACED]->(:Order)-[:CONTAINS]->(p)
                WHERE other <> c AND p IN purchased_products
                
                MATCH (other)-[:PLACED]->(:Order)-[:CONTAINS]->(rec:Product)
                WHERE NOT rec IN purchased_products
                
                RETURN rec.name AS name, rec.price AS price, rec.id AS id, COUNT(rec) AS frequency
                ORDER BY frequency DESC
                LIMIT 5
                """,
                customer_id=customer_id
            ).data() 

            if not result:
                return "Could not generate personalized recommendations based on your purchase history. You might like to check out our top-selling items."

            response_str = "Based on your purchase history, other customers also liked these products. You might too!\n\n"
            for record in result:
                response_str += (
                    f"- Name: {record['name']} (ID: {record['id']})\n"
                    f"  Price: ${record['price']}\n\n"
                )
            
            return response_str