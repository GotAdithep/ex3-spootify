import uuid
from .base import SongGeneratorStrategy

_MOCK_CLIPS = [
    {
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "imageUrl": "https://placehold.co/400x400?text=Mock+Song",
        "duration": 180,
        "prompt": "A mock song generated for offline testing",
    }
]


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    def generate(self, request_data: dict) -> dict:
        task_id = f"mock-{uuid.uuid4().hex[:8]}"
        return {"task_id": task_id, "status": "SUCCESS", "clips": _MOCK_CLIPS}

    def get_status(self, task_id: str) -> dict:
        return {"status": "SUCCESS", "clips": _MOCK_CLIPS}
