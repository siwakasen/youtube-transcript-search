# transcripts.py
import logging
import os
import asyncio
from time import perf_counter
from typing import List
import googleapiclient.discovery
from app.config import config
from app.models import transcripts
from app.models.youtube import ListVideoResponse
from youtube_transcript_api import RequestBlocked, YouTubeTranscriptApi

YTT_API = YouTubeTranscriptApi()
logger = logging.getLogger("uvicorn.error")


async def get_list_transcripts(settings: config.Settings, query: str):
    # get youtube videos from youtube-data-api
    time_youtube_data_api = perf_counter()
    youtube_videos = await get_youtube_videos_by_query(settings, query)
    logger.info(
        f"get_youtube_videos_by_query: {perf_counter() - time_youtube_data_api}"
    )

    # defining task from each youtube videos id
    tasks = [
        process_video_transcript(item.id.videoId, query)
        for item in youtube_videos.items
    ]

    # call all task concurennly with asyncio
    time_before = perf_counter()
    results = await asyncio.gather(*tasks)
    logger.info(f"total times: {perf_counter() - time_before}")

    # flatten
    filtered_transcripts = [t for sub in results for t in sub]

    return filtered_transcripts


async def process_video_transcript(video_id: str, query: str):
    results: List[transcripts.Transcripts] = []

    try:
        # get transcripts data by id
        time_before = perf_counter()
        transcript_data = await get_transcript_by_video_id(video_id)
        logger.info(f'get transcripts "{video_id}": {perf_counter() - time_before}')

        if not transcript_data or not transcript_data.snippets:
            return results

        for snippet in transcript_data.snippets:
            if query in snippet.text:
                results.append(
                    transcripts.Transcripts(
                        text=snippet.text,
                        duration=snippet.duration,
                        videoId=video_id,
                    )
                )
    except RequestBlocked as e:
        logger.warning(e)
        return results
    except Exception as e:
        logger.error(e)
        # optional: logging
        return results

    return results


# Wrap the blocking call with a thred
async def get_transcript_by_video_id(video_id: str):
    return await asyncio.to_thread(_fetch_transcript, video_id)


# YTT_API.fetch is synchronus so it's gonna blocking the event loop
def _fetch_transcript(video_id: str):
    return YTT_API.fetch(video_id, languages=["en"])


async def get_youtube_videos_by_query(
    settings: config.Settings,
    query: str,
) -> ListVideoResponse:
    # env handling
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" if settings.ENV == "DEV" else "0"

    youtube = googleapiclient.discovery.build(
        "youtube",
        "v3",
        developerKey=settings.YOUTUBE_API_KEY,
    )

    request = youtube.search().list(
        part="snippet",
        q=query,
        relevanceLanguage="en",
        type="video",
        videoCaption="closedCaption",
        videoEmbeddable="true",
        maxResults=25,
        order="viewCount",
    )

    raw_response = request.execute()
    response = ListVideoResponse(**raw_response)

    return response
