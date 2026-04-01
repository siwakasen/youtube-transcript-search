# transcripts.py
from typing import List
from pydantic import BaseModel


# TODO: find offset function, if not found remove it
class Transcripts(BaseModel):
    text: str
    duration: float
    videoId: str


class TranscriptsResponse(BaseModel):
    message: str
    query: str
    transcripts: List[Transcripts]
