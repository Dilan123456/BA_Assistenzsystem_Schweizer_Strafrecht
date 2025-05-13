from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import json


load_dotenv()

NEO4J_URI=os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD= os.getenv("NEO4J_PASSWORD", "password")

def get_graph_facts():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    facts = []
    with driver.session() as session:
        result = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.id IS NOT NULL AND b.id IS NOT NULL
            RETURN a.id AS start, type(r) AS relation, b.id AS end
        """)

        for row in result:
            fact = f"'{row['start']}' {row['relation']} '{row['end']}'."
            facts.append(fact)

    return facts

# === Fakten als Textliste speichern ===
def save_facts_to_txt(facts, path="graph_facts.txt"):
    with open(path, "w", encoding="utf-8") as f:
        for fact in facts:
            f.write(fact + "\n")

# === Fakten auch als JSON speichern (optional) ===
def save_facts_to_json(facts, path="graph_facts.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    facts = get_graph_facts()
    print(f"✅ {len(facts)} Fakten extrahiert.")

    save_facts_to_txt(facts)
    save_facts_to_json(facts)
    print("Fakten gespeichert in 'graph_facts.txt' und 'graph_facts.json'")
