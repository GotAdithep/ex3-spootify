import os
from .strategies.base import SongGeneratorStrategy
from .strategies.mock import MockSongGeneratorStrategy
from .strategies.suno import SunoSongGeneratorStrategy


def get_generator_strategy() -> SongGeneratorStrategy:
    strategy = os.getenv("GENERATOR_STRATEGY", "suno").lower()
    if strategy == "mock":
        return MockSongGeneratorStrategy()
    return SunoSongGeneratorStrategy()
