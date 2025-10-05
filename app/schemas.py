from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    text: str
    source: Optional[str] = "manual"
    tags: Optional[List[str]] = []
