from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Song:
    id: str
    title: str
    duration: str = ""        # ← this line is missing

@dataclass
class Album:
    id: str
    title: str
    songs: list[Song] = field(default_factory=list)
    artist: str = ""          # ← check this one too

    def get_song(self, song_id: str) -> Optional[Song]:
        return next((s for s in self.songs if s.id == song_id), None)