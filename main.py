# main.py
import sys
import os

# This ensures the application can find your custom modules
sys.path.append(os.getcwd())

from crew.crew_setup import RetailCrew
from graph_db.driver import Neo4jDriver

def main():
    print("--- AI Retail Assistant (Graph Edition) ---")
    
    # Define a complex query that requires multiple tools
    query = """
    I am customer C001. Can you show me my last couple of orders? 
    Also, what is your policy on returning items? 
    Finally, I'm looking for something to help me relax after work.
    """
    
    print(f"\nCustomer Query:\n{query}")
    
    # Create an instance of the crew with the query
    retail_crew = RetailCrew(query)
    
    # Run the crew and get the result
    print("\n--- Kicking off the crew... ---")
    try:
        result = retail_crew.run()
        
        print("\n--- Crew execution complete! ---")
        print("\nFinal Result:")
        print(result)
        
    except Exception as e:
        print(f"\nAn error occurred during crew execution: {e}")
    finally:
        # Always close the Neo4j connection when done
        Neo4jDriver.close_driver()
        print("\n--- Neo4j connection closed. ---")


if __name__ == "__main__":
    main()