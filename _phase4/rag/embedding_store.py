import chromadb
from chromadb.config import Settings
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_PATH = os.path.join(BASE_DIR, "../chroma_db")

chroma = chromadb.Client(
    Settings(persist_directory=PERSIST_PATH)
)
print("Persist path:", PERSIST_PATH)
collection = chroma.get_or_create_collection("terraform_knowledge")


def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def add_documents(docs):
    for i, doc in enumerate(docs):
        embedding = embed_text(doc)
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )
# Semantic Search
def search(query, k=3):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]