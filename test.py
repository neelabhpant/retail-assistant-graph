# test_tools.py
import sys
import os

sys.path.append(os.getcwd())

from tools.order_history_tool import OrderHistoryTool
from tools.return_item_tool import ReturnItemTool
from tools.faq_tool import FAQTool
from graph_db.driver import Neo4jDriver

def run_tests():
    print("--- Testing Neo4j-Powered Tools ---")
    
    # === Test OrderHistoryTool ===
    print("\n--- Testing OrderHistoryTool ---")
    # ... (code for this test is unchanged) ...
    order_history_tool = OrderHistoryTool()
    print("\n[Test Case 1.1: Valid Customer 'C001']")
    result = order_history_tool.run(customer_id='C001')
    print("Result:")
    print(result)

    # === Test ReturnItemTool ===
    print("\n--- Testing ReturnItemTool ---")
    # ... (code for this test is unchanged) ...
    return_item_tool = ReturnItemTool()
    print("\n[Test Case 2.1: Eligible Return (Delivered Order)]")
    result = return_item_tool.run(customer_id='C001', order_id='12345', product_sku='LP123')
    print("Result:")
    print(result)

    # === Test FAQTool ===
    print("\n--- Testing FAQTool ---")
    faq_tool = FAQTool()
    print("\n[Test Case 3.1: Query about returns]")
    result = faq_tool.run(query="how do I send things back?")
    print("Result:")
    print(result)
    
    print("\n--- All Tests Complete ---")

if __name__ == "__main__":
    try:
        run_tests()
    finally:
        Neo4jDriver.close_driver()