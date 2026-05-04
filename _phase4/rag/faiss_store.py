import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


VECTOR_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "rag/faiss_index"))

print("FAISS DB PATH:", VECTOR_DB_PATH)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# Load index
def semantic_search(query, k=3):
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]