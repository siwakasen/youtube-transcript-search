# transcripts.py
from typing import List
from pydantic import BaseModel


class Transcripts(BaseModel):
    text: str
    duration: float = 0
    videoId: str
    offset: int = 0


class TranscriptsResponse(BaseModel):
    message: str
    query: str
    transcripts: List[Transcripts]
