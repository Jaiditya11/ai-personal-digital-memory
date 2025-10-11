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
    Note right of Notion: Returns pages with<br/>Name + Tags properties
    Notion-->>API: Task list (JSON)
    API->>Chroma: collection.add(ids, documents, metadatas)
    Note right of Chroma: Embeds notes via "all-MiniLM-L6-v2"<br/>and stores vector representations
    API-->>User: Response: status ok, imported count

    %% --- Query Flow ---
    User->>API: GET /query?q=Explain DSA
    Note right of API: Reads query param q="Explain DSA"<br/>and top_k=3 by default
    API->>Chroma: collection.query(query_texts=[q], n_results=top_k)
    Note right of Chroma: Retrieves top 3 similar notes<br/>using cosine similarity
    Chroma-->>API: Matching documents + metadata
    API->>Ollama: POST /api/generate<br/>model=llama3.1:8b<br/>prompt="Context + Question"
    Note right of Ollama: Generates concise natural-language answer
    Ollama-->>API: Returns generated text
    API-->>User: Sends final answer and retrieved results
