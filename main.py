# main.py
from functools import lru_cache
from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, status
from app.models.transcripts import Transcripts, TranscriptsResponse
from app.data.dummy import TRANSCRIPTS_DATA_DUMMY
from app.services.transcripts import searchYoutubeVideos
from app.core import config

app = FastAPI()


@lru_cache
def get_settings():
    s = config.Settings()
    return s


@app.get(
    "/api",
    response_model=TranscriptsResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": TranscriptsResponse,
            "description": "Transcripts not found",
        }
    },
)
async def list(
    settings: Annotated[config.Settings, Depends(get_settings)],
    q: str,
    limit: int = 10,
):
    filtered: List[Transcripts] = [
        Transcripts(**t)
        for t in TRANSCRIPTS_DATA_DUMMY
        if q.lower() in t["text"].lower()
    ]
    if len(filtered) == 0:
        raise HTTPException(
            status_code=404,
            detail=TranscriptsResponse(
                message="Transcripts not found", query=q, transcripts=[]
            ).model_dump(),
        )
    return (
        TranscriptsResponse(
            message="Success getting transcripts", query=q, transcripts=filtered[:limit]
        )
    ).model_dump()


@app.get("/search")
async def search(settings: Annotated[config.Settings, Depends(get_settings)], q: str):
    return await searchYoutubeVideos(settings, q)
