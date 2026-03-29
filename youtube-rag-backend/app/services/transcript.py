from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled

def fetch_transcript(video_id: str) -> str:
    try:
        yyt_api = YouTubeTranscriptApi()
        transcript = yyt_api.fetch(
            video_id=video_id,
            languages=["en", "en-US", "en-GB","hi"]
        )
        return " ".join(chunk.text for chunk in transcript)
    except TranscriptsDisabled :
        return "Transcript is disabled for this video."

