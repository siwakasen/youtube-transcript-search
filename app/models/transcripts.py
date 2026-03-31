# transcripts.py
from typing import List
from pydantic import BaseModel


class Transcripts(BaseModel):
    text: str
    offset: int
    videoId: str


class TranscriptsResponse(BaseModel):
    message: str
    query: str
    transcripts: List[Transcripts]
