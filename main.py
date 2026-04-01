# main.py
from functools import lru_cache
from time import perf_counter
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from app.models.transcripts import TranscriptsResponse
from app.services.pokemon import get_pokemon
from app.services.transcripts import (
    get_list_transcripts,
)
from app.core import config

app = FastAPI()


@lru_cache
def get_settings():
    s = config.Settings()
    return s


@app.get(
    "/api",
    response_model=TranscriptsResponse,
)
async def list(
    settings: Annotated[config.Settings, Depends(get_settings)],
    q: str,
    limit: int = 10,
):
    time_get_list = perf_counter()
    transcripts = await get_list_transcripts(settings, query=q)
    print(f"getListTranscripts take times: {perf_counter() - time_get_list} ")
    if len(transcripts) == 0:
        raise HTTPException(
            status_code=404,
            detail=TranscriptsResponse(
                message="Transcripts not found", query=q, transcripts=[]
            ).model_dump(),
        )
    return (
        TranscriptsResponse(
            message="Success getting transcripts",
            query=q,
            transcripts=transcripts[:limit],
        )
    ).model_dump()


@app.get("/pokemon")
async def captions():
    return await get_pokemon()
