# test_tools.py
import sys
import os

sys.path.append(os.getcwd())

from tools.order_history_tool import OrderHistoryTool
from tools.return_item_tool import ReturnItemTool
from tools.faq_tool import FAQTool
from tools.product_search_tool import ProductSearchTool
from tools.recommendation_tool import RecommendationTool # Import the new tool
from graph_db.driver import Neo4jDriver

def run_tests():

    print("\n--- Testing RecommendationTool ---")
    recommendation_tool = RecommendationTool()
    print("\n[Test Case 5.1] Recommendations for Customer 'C001'")
    print("Result:")
    print(recommendation_tool.run(customer_id='C001'))

    print("\n[Test Case 5.2] Recommendations for Customer 'C002'")
    print("Result:")
    print(recommendation_tool.run(customer_id='C002'))
    
    print("\n--- All Tests Complete ---")

if __name__ == "__main__":
    try:
        run_tests()
    finally:
        Neo4jDriver.close_driver()