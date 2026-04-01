# transcripts.py
from typing import List, Optional
from pydantic import BaseModel


class Transcripts(BaseModel):
    text: str
    duration: Optional[float]
    videoId: str
    offset: Optional[int]


class TranscriptsResponse(BaseModel):
    message: str
    query: str
    transcripts: List[Transcripts]
