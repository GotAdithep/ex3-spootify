import os
import requests
from .base import SongGeneratorStrategy

SUNO_GENERATE_URL = "https://api.sunoapi.org/api/v1/generate"
SUNO_STATUS_URL = "https://api.sunoapi.org/api/v1/generate/record-info"


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, request_data: dict) -> dict:
        mood = request_data.get("mood", "")
        genre = request_data.get("genre", "")
        occasion = request_data.get("occasion", "")
        optional_story = request_data.get("optional_story", "")
        instrumental = request_data.get("instrumental", False)
        singer_voice_type = request_data.get("singer_voice_type", "")
        title = request_data.get("title", "")

        style_desc = f"{genre}, {mood}"
        if occasion:
            style_desc += f", {occasion}"

        callback_url = os.getenv("SUNO_CALLBACK_URL", "https://example.com/callback")

        body = {
            "customMode": False,
            "instrumental": instrumental,
            "model": "V4_5ALL",
            "prompt": f"A {mood} {genre} song for {occasion}. {optional_story}".strip(),
            "style": style_desc,
            "title": title,
            "callBackUrl": callback_url,
        }
        if not instrumental:
            body["vocalGender"] = singer_voice_type

        resp = requests.post(SUNO_GENERATE_URL, json=body, headers=self._headers(), timeout=15)
        json_data = resp.json()

        if json_data.get("code") == 200:
            task_id = json_data["data"]["taskId"]
            return {"task_id": task_id, "status": "PENDING", "clips": None}

        raise RuntimeError(json_data.get("msg", "Suno API generation failed"))

    def get_status(self, task_id: str) -> dict:
        resp = requests.get(
            SUNO_STATUS_URL,
            params={"taskId": task_id},
            headers=self._headers(),
            timeout=10,
        )
        json_data = resp.json()

        if json_data.get("code") != 200:
            raise RuntimeError(json_data.get("msg", "Suno API status check failed"))

        data = json_data["data"]
        suno_status = data.get("status", "PENDING").upper()
        clips = None

        if suno_status == "SUCCESS":
            raw_clips = data.get("response", {}).get("sunoData", [])
            clips = [
                {
                    "audioUrl": c.get("audioUrl", ""),
                    "imageUrl": c.get("imageUrl", ""),
                    "duration": int(c.get("duration") or 0),
                    "prompt": c.get("prompt", ""),
                }
                for c in raw_clips
            ]

        return {"status": suno_status, "clips": clips}
