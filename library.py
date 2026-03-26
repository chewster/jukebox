from models import Album, Song
from typing import Optional

class Library:
    def __init__(self, albums: list[Album]):
        self.albums = {album.id: album for album in albums}

    def get_song(self, selection: str) -> Optional[Song]:
        """Parse a 5-char ID like '01-04' and return the Song, or None."""
        if not self._valid_format(selection):
            return None
        album_id, song_id = selection.split("-")
        album = self.albums.get(album_id)
        if not album:
            return None
        return album.get_song(song_id)

    def _valid_format(self, selection: str) -> bool:
        parts = selection.split("-")
        return (
            len(parts) == 2
            and len(parts[0]) == 2
            and len(parts[1]) == 2
            and all(p.isdigit() for p in parts)
        )

    def list_catalog(self) -> str:
        lines = []
        for album in self.albums.values():
            lines.append(f"[{album.id}] {album.title}")
            for song in album.songs:
                lines.append(f"    [{album.id}-{song.id}] {song.title}")
        return "\n".join(lines)