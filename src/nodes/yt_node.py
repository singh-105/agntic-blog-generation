from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query)["v"][0]

def yt_transcript_node(state):
    url = state["yt_url"]
    video_id = extract_video_id(url)
    
    ytt = YouTubeTranscriptApi()
    
    # list available transcripts, pick first one
    transcript_list = ytt.list(video_id)
    transcript = transcript_list.find_generated_transcript(
        [t.language_code for t in transcript_list]
    )
    fetched = transcript.fetch()
    full_text = " ".join([t.text for t in fetched])
    
    return {"transcript": full_text}