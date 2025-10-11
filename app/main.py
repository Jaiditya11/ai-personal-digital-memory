from fastapi import FastAPI
from app.schemas import IngestRequest
from app.db import collection
import uuid
from app.llm import generate_answer
from app.notion_client import fetch_notion_tasks

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
    task_id = str(uuid.uuid4())

    # Convert tags list -> comma-separated string
    tags_str = ", ".join(data.tags) if data.tags else ""

    # ✅ Build metadata only with non-empty fields
    metadata = {"source": data.source}
    if tags_str:
        metadata["tags"] = tags_str

    collection.add(
        ids=[task_id],
        documents=[data.text],
        metadatas=[metadata],
    )

    return {"status": "stored", "id": task_id}


# ---------------------------------------------------------------------
# Query endpoint – semantic search on stored text
# ---------------------------------------------------------------------
@app.get("/query")
def query_tasks(q: str, top_k: int = 3):
    """
    Retrieves top_k semantically similar documents to query `q`
    and asks the LLM to generate an answer.
    """
    results = collection.query(query_texts=[q], n_results=top_k)
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    # 🔸 Ask the LLM for an answer based on retrieved docs
    answer = generate_answer(docs, q)

    paired_results = list(zip(docs, metas))
    return {"query": q, "results": paired_results, "answer": answer}


@app.post("/sync-notion")
def sync_notion():
    """
    Pulls tasks from Notion DB and ingests them into Chroma.
    """
    tasks = fetch_notion_tasks()
    for t in tasks:
        task_id = str(uuid.uuid4())
        tags_str = ", ".join(t["tags"]) if t["tags"] else ""
        metadata = {"source": t["source"]}
        if tags_str:
            metadata["tags"] = tags_str

        collection.add(
            ids=[task_id],
            documents=[t["text"]],
            metadatas=[metadata],
        )

    return {"status": "ok", "imported": len(tasks)}