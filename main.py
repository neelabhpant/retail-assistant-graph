# main.py
import sys
import os

sys.path.append(os.getcwd())

from crew.crew_setup import RetailCrew
from graph_db.driver import Neo4jDriver

def main():
    print("--- AI Retail Assistant (Graph Edition) ---")

    query = "I'm customer C001. Based on my past purchases, what else might I be interested in?"

    print(f"\nCustomer Query:\n{query}")

    retail_crew = RetailCrew(query)

    print("\n--- Kicking off the crew... ---")
    try:
        result = retail_crew.run()

        print("\n--- Crew execution complete! ---")
        print("\nFinal Result:")
        print(result)

    except Exception as e:
        print(f"\nAn error occurred during crew execution: {e}")
    finally:
        Neo4jDriver.close_driver()
        print("\n--- Neo4j connection closed. ---")


if __name__ == "__main__":
    main()