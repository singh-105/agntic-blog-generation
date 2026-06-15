from typing import TypedDict, Optional
from typing_extensions import TypedDict

class Blog(TypedDict):
    title: str
    content: str

class BlogState(TypedDict):
    topic: str
    yt_url: Optional[str]
    transcript: Optional[str]
    blog: Blog
    current_language: str