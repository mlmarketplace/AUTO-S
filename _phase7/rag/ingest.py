# rag/ingest.py

import os
from dotenv import load_dotenv
from _phase4.rag.chunker import chunk_text
from _phase4.rag.embedding_store import embed_text, collection

load_dotenv()

# -----------------------------
# DATA PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")

print("Loading data from:", DATA_FOLDER)

# -----------------------------
# LOAD DOCUMENTS
# -----------------------------
def load_documents():
    documents = []

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".txt"):
            file_path = os.path.join(DATA_FOLDER, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

                documents.append({
                    "text": text,
                    "source": file
                })

    print(f"Loaded {len(documents)} documents")
    return documents


# -----------------------------
# SPLIT INTO CHUNKS
# -----------------------------
def split_into_chunks(documents):
    chunks = []

    for doc in documents:
        doc_chunks = chunk_text(doc["text"], chunk_size=150, overlap=30)

        for chunk in doc_chunks:
            chunks.append({
                "text": chunk,
                "source": doc["source"]
            })

    print(f"Created {len(chunks)} chunks")
    return chunks


# -----------------------------
# STORE EMBEDDINGS
# -----------------------------
def store_embeddings(chunks):
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk["text"])

        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            ids=[f"{chunk['source']}_{i}"],
            metadatas=[{"source": chunk["source"]}]
        )

    print(f"Stored {len(chunks)} embeddings in ChromaDB")


# -----------------------------
# MAIN
# -----------------------------
def ingest():
    documents = load_documents()
    chunks = split_into_chunks(documents)
    store_embeddings(chunks)

    print("✅ Knowledge base successfully persisted and indexed (ChromaDB)")


if __name__ == "__main__":
    ingest()