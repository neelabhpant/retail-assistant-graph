# test_tools.py
import sys
import os

sys.path.append(os.getcwd())

from tools.order_history_tool import OrderHistoryTool
from tools.return_item_tool import ReturnItemTool
from tools.faq_tool import FAQTool
from tools.product_search_tool import ProductSearchTool
from graph_db.driver import Neo4jDriver

def run_tests():
    print("--- Testing All Neo4j-Powered Tools ---")
    
    # === Test OrderHistoryTool ===
    print("\n--- Testing OrderHistoryTool ---")
    order_history_tool = OrderHistoryTool()
    print("[Test Case 1.1] Valid Customer 'C001'")
    print("Result:")
    print(order_history_tool.run(customer_id='C001'))
    
    # === Test ReturnItemTool ===
    print("\n--- Testing ReturnItemTool ---")
    return_item_tool = ReturnItemTool()
    print("\n[Test Case 2.1] Eligible Return")
    print("Result:")
    print(return_item_tool.run(customer_id='C001', order_id='12345', product_sku='LP123'))
    
    # === Test FAQTool ===
    print("\n--- Testing FAQTool ---")
    faq_tool = FAQTool()
    print("\n[Test Case 3.1] Query about returns")
    print("Result:")
    print(faq_tool.run(query="how do I send things back?"))

    # === Test ProductSearchTool ===
    print("\n--- Testing ProductSearchTool ---")
    product_search_tool = ProductSearchTool()
    print("\n[Test Case 4.1] Query for a computer")
    print("Result:")
    print(product_search_tool.run(query="a computer for my office"))
    
    print("\n--- All Tests Complete ---")

if __name__ == "__main__":
    try:
        run_tests()
    finally:
        Neo4jDriver.close_driver()