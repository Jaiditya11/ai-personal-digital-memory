import os
import chromadb
from chromadb.utils import embedding_functions

# Directory to persist the DB
PERSIST_DIR = os.getenv("CHROMA_DIR", "./data/chroma")
os.makedirs(PERSIST_DIR, exist_ok=True)

# Initialize Chroma client
client = chromadb.PersistentClient(path=PERSIST_DIR)

# Embedding function (small, free model)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create or get collection
collection = client.get_or_create_collection(
    name="tasks",
    embedding_function=ef,
    metadata={"hnsw:space": "cosine"}
)
