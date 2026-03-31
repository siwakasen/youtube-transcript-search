# youtube.py
from typing import List

from pydantic import BaseModel


class PageInfo(BaseModel):
    totalResults: int
    resultsPerPage: int


class Id(BaseModel):
    kind: str
    videoId: str


class Default(BaseModel):
    url: str
    width: int
    height: int


class Medium(BaseModel):
    url: str
    width: int
    height: int


class High(BaseModel):
    url: str
    width: int
    height: int


class Thumbnails(BaseModel):
    default: Default
    medium: Medium
    high: High


class Snippet(BaseModel):
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    liveBroadcastContent: str
    publishTime: str


class Item(BaseModel):
    kind: str
    etag: str
    id: Id
    snippet: Snippet


class ListVideoResponse(BaseModel):
    kind: str
    etag: str
    nextPageToken: str
    regionCode: str
    pageInfo: PageInfo
    items: List[Item]
