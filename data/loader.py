import json
from pathlib import Path
from models import Song, Album
from library import Library


def load_library(path: str = "data/albums.json") -> Library:
    raw = Path(path).read_text()
    data = json.loads(raw)

    albums = []
    for album_index, album_data in enumerate(data["albums"]):
        album_id = f"{album_index + 1:02d}"  # "01", "02", ...

        songs = []
        for song_index, song_data in enumerate(album_data["songs"]):
            song_id = f"{song_index + 1:02d}"  # "01", "02", ...
            songs.append(Song(
                id=song_id,
                title=song_data["title"],
                duration=song_data["duration"],
            ))

        albums.append(Album(
            id=album_id,
            title=album_data["title"],
            artist=album_data["artist"],
            songs=songs,
        ))

    return Library(albums)