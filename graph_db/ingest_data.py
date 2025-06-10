# graph_db/ingest_data.py
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from graph_db.driver import neo4j_driver, Neo4jDriver
from config.config import settings
import time

def ingest_data():
    """
    The main function to ingest all data into Neo4j, create embeddings,
    and set up the vector index.
    """
    print("Starting data ingestion process...")
    embedding_model = SentenceTransformer(settings.embedding_model_name)

    with neo4j_driver.session() as session:
        # Create constraints for unique nodes
        print("Creating uniqueness constraints...")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Customer) REQUIRE c.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (o:Order) REQUIRE o.id IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (f:FAQ) REQUIRE f.id IS UNIQUE")

        # Ingest structured data (Customers, Products, Orders)
        print("Ingesting structured data (Customers, Products, Orders)...")
        ingest_customer_order_data(session)

        # Ingest unstructured data (FAQs) and create embeddings
        print("Ingesting unstructured data (FAQs)...")
        faqs = ingest_faq_data(session, embedding_model)

        # Create product embeddings from the ingested products
        print("Creating and storing product embeddings...")
        create_product_embeddings(session, embedding_model)

        # Create vector indexes
        print("Creating vector indexes for FAQs and Products...")
        create_vector_indexes(session)

    print("Data ingestion process complete!")

def ingest_customer_order_data(session):
    """Reads customer and order data from JSON and ingests into Neo4j."""
    with open('data/orders.json', 'r') as f:
        orders_data = json.load(f)

    for record in orders_data:
        # Create Customer node
        session.run(
            """
            MERGE (c:Customer {id: $customer_id})
            SET c.name = $name
            """,
            customer_id=record['customer_id'],
            name=record['name']
        )

        for order in record['orders']:
            # Create Order node
            session.run(
                """
                MERGE (o:Order {id: $order_id})
                SET o.date = $date, o.status = $status
                """,
                order_id=order['order_id'],
                date=order['date'],
                status=order['status']
            )

            # Link Customer to Order
            session.run(
                """
                MATCH (c:Customer {id: $customer_id})
                MATCH (o:Order {id: $order_id})
                MERGE (c)-[:PLACED]->(o)
                """,
                customer_id=record['customer_id'],
                order_id=order['order_id']
            )

            for item in order['items']:
                # Create Product node and link to Order
                session.run(
                    """
                    MATCH (o:Order {id: $order_id})
                    MERGE (p:Product {id: $product_sku})
                    ON CREATE SET p.name = $product_name, p.price = $price
                    MERGE (o)-[:CONTAINS]->(p)
                    """,
                    order_id=order['order_id'],
                    product_sku=item['sku'],
                    product_name=item['name'],
                    price=item['price']
                )

def ingest_faq_data(session, model):
    """Reads FAQs from text file, creates embeddings, and ingests."""
    with open('data/faqs.txt', 'r') as f:
        faqs = [qa.strip() for qa in f.read().split('---') if qa.strip()]

    for i, faq in enumerate(faqs):
        embedding = model.encode(faq).tolist()
        session.run(
            """
            MERGE (f:FAQ {id: $id})
            SET f.text = $text, f.embedding = $embedding
            """,
            id=f"faq_{i}",
            text=faq,
            embedding=embedding
        )
    return faqs

def create_product_embeddings(session, model):
    """Adds categories to products from CSV and creates embeddings."""
    df_products = pd.read_csv('data/products.csv')

    for _, row in df_products.iterrows():
        description = (
            f"Product Name: {row['name']}, Category: {row['category']}, "
            f"Description: {row['description']}"
        )
        embedding = model.encode(description).tolist()

        session.run(
            """
            MATCH (p:Product {id: $id})
            SET p.category = $category, p.description = $description, p.embedding = $embedding
            """,
            id=row['product_id'],
            category=row['category'],
            description=description,
            embedding=embedding
        )

def create_vector_indexes(session):
    """Creates vector indexes on the FAQ and Product nodes."""
    # Vector index for FAQs
    session.run(
        """
        CREATE VECTOR INDEX faq_index IF NOT EXISTS
        FOR (f:FAQ) ON (f.embedding)
        OPTIONS {indexConfig: {
            `vector.dimensions`: 384,
            `vector.similarity_function`: 'cosine'
        }}
        """
    )

    # Vector index for Products
    session.run(
        """
        CREATE VECTOR INDEX product_index IF NOT EXISTS
        FOR (p:Product) ON (p.embedding)
        OPTIONS {indexConfig: {
            `vector.dimensions`: 384,
            `vector.similarity_function`: 'cosine'
        }}
        """
    )
    print("Waiting for indexes to populate...")
    session.run("CALL db.awaitIndexes(300)")


if __name__ == "__main__":
    ingest_data()
    Neo4jDriver.close_driver()