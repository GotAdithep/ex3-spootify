from apps.song.models import Song
from .models import SongGenRequest


def create_song_from_clips(song_request: SongGenRequest, clips: list) -> Song | None:
    if not clips:
        return None
    clip = clips[0]
    song = Song.objects.create(
        title=song_request.song_title,
        duration=clip.get("duration", 0),
        song_url=clip.get("audioUrl", ""),
        image_url=clip.get("imageUrl", ""),
        lyrics=clip.get("prompt", ""),
        user=song_request.user,
    )
    song_request.song = song
    song_request.generation_status = SongGenRequest.Generation_Status.SUCCESS
    song_request.save()
    return song
