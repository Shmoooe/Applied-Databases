from neo4j import GraphDatabase


def connect_neo4j():
    uri = "neo4j://localhost:7687"
    try:
        driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4jneo4j"), max_connection_lifetime=1000)
        with driver.session() as session:
            session.run("RETURN 1")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        return None

        
if __name__ == "__main__":
    connect_neo4j()