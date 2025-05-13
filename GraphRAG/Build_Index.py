from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
import json

#Umgebungsvariablen laden
load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

#Fakten aus JSON laden
with open("graph_facts.json", "r", encoding="utf-8") as f:
    faktentexte = json.load(f)

#In LangChain-Dokumente umwandeln
docs = [Document(page_content=f) for f in faktentexte]

#Embedding-Modell initialisieren
embeddings = OpenAIEmbeddings()

#FAISS-Vektorindex erstellen und speichern
vectordb = FAISS.from_documents(docs, embeddings)
vectordb.save_local("faiss_knowledgegraph_index")

print(f" {len(docs)} Fakten verarbeitet und Vektorindex gespeichert unter 'faiss_knowledgegraph_index'")
