import os
import httpx

# 1️⃣  Defaults — these can be overridden by environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("LLM_MODEL", "llama3.1:8b")

def generate_answer(context: list[str], question: str) -> str:
    """
    Ask the Ollama local model to answer `question` based on `context`.
    If Ollama isn't running, return a fallback summary.
    """

    # 2️⃣  Combine top documents into one text block
    context_text = "\n".join(context[:3]) if context else "No context found."
    prompt = f"Context:\n{context_text}\n\nQuestion: {question}\n\nAnswer concisely:"

    # 3️⃣  Send request to Ollama REST API
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                OLLAMA_URL,
                json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            data = response.json()
            # 4️⃣  Return only the generated text
            return data.get("response", "").strip() or "(No answer generated)"
    except Exception as e:
        # 5️⃣  Graceful fallback if Ollama isn’t running
        print(f"[WARN] Ollama not available: {e}")
        return f"(LLM offline) Context summary:\n{context_text}"
