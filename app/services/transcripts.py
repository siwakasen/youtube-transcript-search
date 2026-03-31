# transcripts.py
import os

import googleapiclient.discovery

from app.core import config
from app.models.youtube import ListVideoResponse


async def searchYoutubeVideos(
    settings: config.Settings,
    query: str,
):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" if settings.ENV == "DEV" else "0"

    api_service_name = "youtube"
    api_version = "v3"
    print(settings.YOUTUBE_API_KEY)
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
        maxResults=5,
    )
    response: ListVideoResponse = request.execute()

    return response


async def call_youtube_transcript_api(videoId: str):
    pass
