# rag/embedding_store.py

import chromadb
from chromadb.config import Settings
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# PERSIST PATH (CLEAN + RELIABLE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PERSIST_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "chroma_db"))

print("Persist path:", PERSIST_PATH)

# -----------------------------
# CHROMA CLIENT (PERSISTENT)
# -----------------------------
chroma = chromadb.Client(
    Settings(
        persist_directory=PERSIST_PATH
    )
)

collection = chroma.get_or_create_collection("terraform_knowledge")

# -----------------------------
# EMBEDDING FUNCTION
# -----------------------------
def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# -----------------------------
# SEMANTIC SEARCH
# -----------------------------
def search(query, k=3):
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results.get("documents", [[]])[0]