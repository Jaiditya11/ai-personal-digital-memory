# AI Personal Digital Memory
## AI Personal Digital Memory – Query Flow

```mermaid
sequenceDiagram
    participant Notion as 🗂 Notion Database
    participant API as ⚙️ FastAPI App (app.main)
    participant Chroma as 🧮 Vector DB (Chroma)
    participant Ollama as 🧠 LLM (llama3.1:8b)
    participant User as 🧑‍💻 User / Client (curl or browser)

    %% --- Data Sync Flow ---
    User->>API: POST /sync-notion
    API->>Notion: GET /databases/{DATABASE_ID}/query
    Note right of Notion: Notion API returns pages<br/>with Name + Tags properties
    Notion-->>API: {"results": [...]} (task list)
    API->>Chroma: collection.add(ids, documents, metadatas)
    Note right of Chroma: Embeds each note via<br/>"all-MiniLM-L6-v2" and stores vectors
    API-->>User: {"status":"ok","imported":N}

    %% --- Query Flow ---
    User->>API: GET /query?q=Explain DSA
    Note right of API: FastAPI reads query params<br/>q="Explain DSA", top_k=3 (default)
    API->>Chroma: collection.query(query_texts=[q], n_results=top_k)
    Note right of Chroma: Retrieve top 3 similar notes<br/>based on cosine similarity
    Chroma-->>API: {"documents":[["Revise DSA Topics"]], "metadatas":[[{"source":"notion"}]]}

    API->>Ollama: POST /api/generate<br/>model=llama3.1:8b<br/>prompt="Context: {docs}\\nQuestion: {q}"
    Note right of Ollama: LLM reads context + question<br/>Generates concise answer
    Ollama-->>API: {"response":"DSA covers data structures and algorithms for coding interviews."}

    API-->>User: JSON Response<br/>{
        "query": q,
        "results": [(doc, metadata), ...],
        "answer": "DSA covers data structures and algorithms..."
    }
