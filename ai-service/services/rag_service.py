from sentence_transformers import SentenceTransformer
import chromadb
import re
import os


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection("rag_docs")


def load_documents(file_path):
    with open(file_path, "r") as f:
        return f.read()

def chunk_text(text, chunk_size=200, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += (chunk_size - overlap)

    return chunks

def store_embeddings(chunks):
    global collection

    try:
        client.delete_collection(name="controls")
    except:
        pass

    collection = client.get_or_create_collection(name="controls")

    embeddings = embedding_model.encode(chunks)
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i].tolist()],
            ids=[f"id_{i}"]
        )

def embed(text):
    return embedding_model.encode(text).tolist()

def run_rag_pipeline():
    DATA_FOLDER = "data"

    documents = []

    for filename in os.listdir(DATA_FOLDER):
        filepath = os.path.join(DATA_FOLDER, filename)

        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                documents.append(f.read())

    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    store_embeddings(all_chunks)

    print(f"RAG pipeline completed. Stored {len(all_chunks)} chunks.")

def retrieve(query):
    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    return results.get("documents", [[]])[0]