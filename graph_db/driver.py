# graph_db/driver.py
from neo4j import GraphDatabase
from config.config import settings

class Neo4jDriver:
    _driver = None

    @classmethod
    def get_driver(cls):
        """
        Returns a singleton instance of the Neo4j driver.
        """
        if cls._driver is None:
            try:
                cls._driver = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_username, settings.neo4j_password)
                )
                cls._driver.verify_connectivity()
                print("Successfully connected to Neo4j.")
            except Exception as e:
                print(f"Failed to connect to Neo4j: {e}")
                raise
        return cls._driver

    @classmethod
    def close_driver(cls):
        """
        Closes the Neo4j driver connection if it exists.
        """
        if cls._driver is not None:
            cls._driver.close()
            cls._driver = None
            print("Neo4j connection closed.")

# You can get an instance of the driver to be used across the application
neo4j_driver = Neo4jDriver.get_driver()