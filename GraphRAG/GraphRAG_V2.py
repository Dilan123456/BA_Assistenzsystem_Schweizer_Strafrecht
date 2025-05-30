from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Umgebungsvariablen laden
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Lade Embedding-Modell und Vektorindex
embeddings = OpenAIEmbeddings()
vectordb = FAISS.load_local("faiss_knowledgegraph_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# Lade Fallfrage aus Textdatei
with open("frage.txt", "r", encoding="utf-8") as f:
    sachverhalt = f.read().strip()

# STRUKTURIERTER PROMPT
template = """
Du bist ein juristischer Assistent im Bereich des Schweizer Strafrechts. Prüfe den folgenden Fall nach dem Gutachtenstil.

Verwende diese Struktur:
1. Relevanter Straftatbestand inkl. Artikel (z.B. Art. 190 oder 193 StGB)
2. Objektiver Tatbestand – Definition + Subsumtion mit dem Sachverhalt
3. Subjektiver Tatbestand – Vorsatz, Eventualvorsatz etc.
4. Rechtswidrigkeit
5. Schuld
6. Ergebnis

Wenn du relevante Informationen aus dem folgenden Kontext (Knowledge Graph) brauchst, baue sie explizit in deine Argumentation ein.

### Kontextwissen (Knowledge Graph):
{context}

### Fallfrage:
{question}
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# Verbinde Retrieval mit GPT-4o und Prompt
llm = ChatOpenAI(model_name="gpt-4o")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# Starte die Prüfung
antwort = qa_chain.run({"query": sachverhalt})

print("\nAntwort des Assistenzsystems:\n")
print(antwort)
