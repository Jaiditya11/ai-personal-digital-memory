from fastapi import FastAPI
from app.schemas import IngestRequest

app = FastAPI()

# In-memory store for now
MEMORY = []

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(data: IngestRequest):
    item = data.model_dump()
    MEMORY.append(item)
    return {"status": "stored", "count": len(MEMORY)}
