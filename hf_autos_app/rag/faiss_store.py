from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

VECTOR_DB_PATH = "rag/faiss_index"


def load_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


vectorstore = load_vectorstore()


def semantic_search(query, k=3):
    docs = vectorstore.similarity_search(query, k=k)
    return [d.page_content for d in docs]