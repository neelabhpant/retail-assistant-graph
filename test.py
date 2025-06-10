# test_tools.py
import sys
import os

sys.path.append(os.getcwd())

from tools.order_history_tool import OrderHistoryTool
from tools.return_item_tool import ReturnItemTool
from graph_db.driver import Neo4jDriver

def run_tests():
    print("--- Testing Neo4j-Powered Tools ---")
    
    # === Test OrderHistoryTool ===
    print("\n--- Testing OrderHistoryTool ---")
    order_history_tool = OrderHistoryTool()
    print("\n[Test Case 1.1: Valid Customer 'C001']")
    result = order_history_tool.run(customer_id='C001')
    print("Result:")
    print(result)
    
    # === Test ReturnItemTool ===
    print("\n--- Testing ReturnItemTool ---")
    return_item_tool = ReturnItemTool()

    print("\n[Test Case 2.1: Eligible Return (Delivered Order)]")
    result = return_item_tool.run(customer_id='C001', order_id='12345', product_sku='LP123')
    print("Result:")
    print(result)

    print("\n[Test Case 2.2: Ineligible Return (Shipped Order)]")
    result = return_item_tool.run(customer_id='C001', order_id='12346', product_sku='NCH789')
    print("Result:")
    print(result)

    print("\n[Test Case 2.3: Item Not Found in Order]")
    result = return_item_tool.run(customer_id='C001', order_id='12345', product_sku='XYZ999')
    print("Result:")
    print(result)
    
    print("\n--- All Tests Complete ---")

if __name__ == "__main__":
    try:
        run_tests()
    finally:
        Neo4jDriver.close_driver()