# AI Personal Digital Memory
sequenceDiagram
    participant User as 🧑 User / Client (curl / browser)
    participant API as ⚙️ FastAPI App (app.main)
    participant Chroma as 🧮 Vector DB (Chroma)
    participant Ollama as 🧠 LLM (llama3.1:8b)

    User->>API: GET /query?q=Explain AWS S3
    Note right of API: FastAPI reads query params<br/>q="Explain AWS S3", top_k=3 (default)

    API->>Chroma: collection.query(query_texts=[q], n_results=top_k)
    Note right of Chroma: • Embed q via "all-MiniLM-L6-v2"<br/>• Retrieve top 3 similar documents<br/>• Return documents + metadata

    Chroma-->>API: {"documents":[["Learn AWS S3 basics"]], "metadatas":[[{"source":"notion","tags":"AWS, learning"}]]}

    API->>API: docs = results["documents"][0]<br/>metas = results["metadatas"][0]
    API->>Ollama: POST /api/generate<br/>model=llama3.1:8b<br/>prompt = f"Context: {docs}\\nQuestion: {q}"

    Note right of Ollama: LLM reads context + question<br/>→ Generates concise natural-language answer

    Ollama-->>API: {"response": "AWS S3 is a cloud-based object storage service..."}

    API->>User: JSON Response<br/>{
      "query": q,
      "results": [(doc, metadata), ...],
      "answer": LLM_text
    }
