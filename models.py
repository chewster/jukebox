from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Song:
    id: str        # e.g. "04"
    title: str

@dataclass
class Album:
    id: str        # e.g. "01"
    title: str
    songs: list[Song] = field(default_factory=list)

    def get_song(self, song_id: str) -> Optional[Song]:
        return next((s for s in self.songs if s.id == song_id), None)