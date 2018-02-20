import os

from neo4j.v1 import GraphDatabase, basic_auth

host = os.environ.get("NEO4J_HOST", "bolt://localhost")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo")
driver = GraphDatabase.driver(host, auth=basic_auth(user, password))


def clear_db():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


clear_db()
