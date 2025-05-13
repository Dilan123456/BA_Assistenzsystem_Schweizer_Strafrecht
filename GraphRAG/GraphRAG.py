from langchain.chains import RetrievalQA
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Lade Embedding-Modell
embeddings = OpenAIEmbeddings()

# Lade FAISS-Vektorindex
vectordb = FAISS.load_local("faiss_knowledgegraph_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever()

# Schritt 4: Verbinde Retriever mit GPT
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    retriever=retriever
)

# Schritt 5: Nutzerfrage stellen
frage = input("Was möchtest du über das Strafrecht wissen? ")
antwort = qa_chain.run(frage)

print("\n Antwort des Systems:")
print(antwort)
