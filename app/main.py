from fastapi import FastAPI
from app.schemas import IngestRequest
from app.db import collection
import uuid

app = FastAPI(title="AI Personal Digital Memory API")


# ---------------------------------------------------------------------
# Health check – confirms the server is running
# ---------------------------------------------------------------------
@app.get("/health")
def health_check():
    """
    Basic health endpoint to verify that the API is up.
    Returns: {"status": "ok"}
    """
    return {"status": "ok"}


# ---------------------------------------------------------------------
# Ingest endpoint – adds text/tasks into the vector database
# ---------------------------------------------------------------------
@app.post("/ingest")
def ingest(data: IngestRequest):
    """
    Accepts a JSON body containing a text snippet (task, note, idea)
    and stores it in the ChromaDB collection as a vector embedding.
    """

    # Generate a unique ID for each ingested document
    task_id = str(uuid.uuid4())

    # Convert tags list -> comma-separated string
    tags_str = ", ".join(data.tags) if data.tags else None

    # Add document + metadata into Chroma
    collection.add(
        ids=[task_id],
        documents=[data.text],
        metadatas=[{
            "source": data.source,
            "tags": tags_str
        }],
    )

    return {"status": "stored", "id": task_id}


# ---------------------------------------------------------------------
# Query endpoint – semantic search on stored text
# ---------------------------------------------------------------------
@app.get("/query")
def query_tasks(q: str, top_k: int = 3):
    """
    Retrieves the most semantically similar documents to the query `q`.
    Uses cosine similarity via the ChromaDB vector index.
    """

    # Search for top_k closest vectors to the query text
    results = collection.query(query_texts=[q], n_results=top_k)

    # Extract documents and metadata (Chroma returns nested lists)
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    # Combine document text with metadata for clarity
    paired_results = list(zip(docs, metas))

    return {
        "query": q,
        "results": paired_results
    }
