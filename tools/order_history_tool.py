# tools/order_history_tool.py
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from graph_db.driver import neo4j_driver

class OrderHistoryInput(BaseModel):
    """Input model for the OrderHistoryTool."""
    customer_id: str = Field(description="The unique identifier of the customer (e.g., C001).")

class OrderHistoryTool(BaseTool):
    name: str = "Order History Tool"
    description: str = "Looks up the complete order history for a given customer ID from the graph database."
    args_schema: Type[BaseModel] = OrderHistoryInput

    def _run(self, customer_id: str) -> str:
        """Executes a Cypher query to retrieve order history from Neo4j."""
        with neo4j_driver.session() as session:

            result = session.run(
                """
                MATCH (c:Customer {id: $customer_id})-[:PLACED]->(o:Order)
                MATCH (o)-[:CONTAINS]->(p:Product)
                RETURN c.name AS customer_name, o, p
                ORDER BY o.date DESC
                """,
                customer_id=customer_id
            )

            orders = {}
            customer_name = ""
            for record in result:
                customer_name = record["customer_name"]
                order_id = record["o"]["id"]
                if order_id not in orders:
                    orders[order_id] = {
                        "date": record["o"]["date"],
                        "status": record["o"]["status"],
                        "items": []
                    }
                orders[order_id]["items"].append({
                    "name": record["p"]["name"],
                    "price": record["p"]["price"]
                })

            if not orders:
                return f"No order history found for customer with ID '{customer_id}'."

            history_str = f"Order history for {customer_name} (ID: {customer_id}):\n"
            for order_id, order_details in orders.items():
                history_str += f"- Order ID: {order_id}, Date: {order_details['date']}, Status: {order_details['status']}\n"
                for item in order_details['items']:
                    history_str += f"  - Item: {item['name']}, Price: ${item['price']}\n"
            return history_str