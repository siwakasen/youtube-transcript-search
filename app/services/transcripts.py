# transcripts.py
import os
from typing import List

import googleapiclient.discovery

from app.core import config
from app.models import transcripts
from app.models.youtube import ListVideoResponse
from youtube_transcript_api import YouTubeTranscriptApi


async def searchYoutubeVideos(
    settings: config.Settings,
    query: str,
):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" if settings.ENV == "DEV" else "0"

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=settings.YOUTUBE_API_KEY
    )

    request = youtube.search().list(
        part="snippet",
        q=query,
        relevanceLanguage="en",
        type="video",
        videoCaption="closedCaption",
        videoDuration="any",
        videoEmbeddable="true",
        maxResults=2,
    )
    raw_response = request.execute()
    response = ListVideoResponse(**raw_response)
    filteredTranscripts: List[transcripts.Transcripts] = []

    # TODO: use concurency
    for i in range(len(response.items)):
        videoId = response.items[i].id.videoId
        raw_transctipts_data = await getTranscriptByVideoId(videoId)
        list_transcripts = raw_transctipts_data.snippets

        # FIX: name variables
        for j in range(len(list_transcripts)):
            if query in list_transcripts[j].text.lower():
                filteredTranscripts.append(
                    transcripts.Transcripts(
                        text=list_transcripts[j].text, offset=0, videoId=videoId
                    )
                )
    return filteredTranscripts


async def getTranscriptByVideoId(video_id: str):
    # FIX: No transcripts were found for any of the requested language codes: ['en']
    # eventhough videoId already searched from youtube data api

    ytt_api = YouTubeTranscriptApi()
    fetched_transcripts = ytt_api.fetch(video_id, languages=["en"])
    return fetched_transcripts
