from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = "faiss_index"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Load index
vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

def semantic_search(query, k=3):
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]