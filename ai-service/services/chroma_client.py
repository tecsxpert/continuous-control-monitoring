import chromadb
from chromadb.utils import embedding_functions

class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_data")

        try:
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        except Exception as e:
            print("Error loading embedding model:", e)
            self.embedding_function = None

        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_function
        )

    def add_documents(self, docs):
        for index, doc in enumerate(docs):
            self.collection.add(
                documents=[doc],
                ids=[str(index)]
            )

    def search(self, query_text):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=2
        )

        return results["documents"][0]
    
    def get_document_count(self):
         return self.collection.count()