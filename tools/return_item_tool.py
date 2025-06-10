# tools/return_item_tool.py
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from graph_db.driver import neo4j_driver

class ReturnItemInput(BaseModel):
    """Input for the ReturnItemTool."""
    customer_id: str = Field(description="The customer's unique identifier.")
    order_id: str = Field(description="The unique identifier of the order.")
    product_sku: str = Field(description="The unique SKU of the product to be returned.")

class ReturnItemTool(BaseTool):
    name: str = "Return Item Tool"
    description: str = "Processes a return request for a specific item from a customer's order by checking the graph database."
    args_schema: Type[BaseModel] = ReturnItemInput

    def _run(self, customer_id: str, order_id: str, product_sku: str) -> str:
        with neo4j_driver.session() as session:
            # This Cypher query validates that the customer placed the order,
            # the order contains the item, and then checks the order's status.
            result = session.run(
                """
                MATCH (c:Customer {id: $customer_id})-[:PLACED]->(o:Order {id: $order_id})
                MATCH (o)-[:CONTAINS]->(p:Product {id: $product_sku})
                RETURN o.status AS status, p.name AS item_name
                """,
                customer_id=customer_id,
                order_id=order_id,
                product_sku=product_sku
            ).single() # We expect only one result or none

            if not result:
                return f"Error: Could not validate the request. Please ensure customer ID '{customer_id}', order ID '{order_id}', and product SKU '{product_sku}' are all correct."

            status = result["status"]
            item_name = result["item_name"]
            
            if status == "Delivered":
                return f"Return approved for item: '{item_name}' (SKU: {product_sku}) from order {order_id}. Please follow the instructions sent to your email."
            else:
                return f"Return denied for item: '{item_name}' (SKU: {product_sku}). Reason: The order status is '{status}', not 'Delivered'."