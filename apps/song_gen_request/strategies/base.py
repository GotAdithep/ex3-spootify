from abc import ABC, abstractmethod


class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request_data: dict) -> dict:
        """
        Start a generation job.

        Args:
            request_data: dict with keys: title, mood, genre, occasion,
                          singer_voice_type, optional_story, instrumental

        Returns:
            dict with keys:
                task_id (str)
                status  (str)  — e.g. "PENDING" or "SUCCESS"
                clips   (list | None) — present when status is SUCCESS
        """

    @abstractmethod
    def get_status(self, task_id: str) -> dict:
        """
        Check the status of a previously started generation job.

        Returns:
            dict with keys:
                status (str)  — e.g. "PENDING", "SUCCESS"
                clips  (list | None)
        """
