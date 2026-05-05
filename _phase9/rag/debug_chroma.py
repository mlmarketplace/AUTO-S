# rag/debug_chroma.py

from _phase4.rag.embedding_store import collection, search

# -----------------------------------------
# INSPECT STORED DOCUMENTS
# -----------------------------------------
def inspect_db():
    data = collection.get()

    documents = data.get("documents", [])

    print(f"\nTotal documents stored: {len(documents)}\n")

    for i, doc in enumerate(documents):
        print(f"--- Document {i+1} ---")
        print(doc[:200])  # preview first 200 chars
        print()


# -----------------------------------------
# TEST SEMANTIC SEARCH
# -----------------------------------------
def test_search(query):
    print(f"\nQuery: {query}\n")

    results = search(query)

    if not results:
        print("No results found ❌\n")
        return

    print("Top Results:\n")

    for i, r in enumerate(results):
        print(f"{i+1}. {r}\n")


# -----------------------------------------
# ADVANCED: SHOW DISTANCES (OPTIONAL)
# -----------------------------------------
def test_search_with_scores(query):
    from _phase4.rag.embedding_store import embed_text

    print(f"\nQuery (with scores): {query}\n")

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for i, (doc, dist) in enumerate(zip(docs, distances)):
        print(f"{i+1}. Distance: {dist}")
        print(doc)
        print()


# -----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":
    inspect_db()

    # Basic tests
    test_search("terraform state lock issue")
    test_search("missing tags policy")
    test_search("reduce cloud cost")

    # Negative test (important for evaluation)
    test_search("kubernetes deployment error")

    # Optional: with similarity scores
    test_search_with_scores("terraform state lock")