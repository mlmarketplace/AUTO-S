import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DATA_FOLDER = "../data"
VECTOR_DB_PATH = "faiss_index"

# -----------------------------
# LOAD FILES
# -----------------------------
documents = []

for file in os.listdir(DATA_FOLDER):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_FOLDER, file), "r") as f:
            text = f.read()
            documents.append(text)

print(f"Loaded {len(documents)} documents")

# -----------------------------
# SPLIT TEXT
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.create_documents(documents)

print(f"Created {len(chunks)} chunks")

# -----------------------------
# EMBEDDINGS
# -----------------------------
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# -----------------------------
# CREATE FAISS INDEX
# -----------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)

# -----------------------------
# SAVE
# -----------------------------
vectorstore.save_local(VECTOR_DB_PATH)

print("✅ FAISS index created and saved")