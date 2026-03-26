from library import Library
from credits import CreditSystem
from play_queue import PlayQueue
from models import Song
from typing import Optional

class Jukebox:
    def __init__(self, library: Library):
        self.library = library
        self.credits = CreditSystem()
        self.queue = PlayQueue()
        self.free_play = False  # stretch goal toggle

    def insert_money(self, dollars: int) -> str:
        new_balance = self.credits.purchase(dollars)
        return f"Credits added. New balance: {new_balance}"

    def select_song(self, selection: str) -> str:
        song = self.library.get_song(selection)
        if song is None:
            return f"Error: '{selection}' is not a valid song ID."
        if not self.free_play and not self.credits.spend(1):
            return "Error: Insufficient credits."
        self.queue.enqueue(song)
        return f"Added to queue: {song.title}"

    def now_playing(self) -> str:
        song = self.queue.now_playing
        return f"Now playing: {song.title}" if song else "Nothing is playing."

    def up_next(self) -> str:
        song = self.queue.up_next
        return f"Up next: {song.title}" if song else "Nothing up next."

    def list_catalog(self) -> str:
        return self.library.list_catalog()

    def toggle_free_play(self) -> str:
        self.free_play = not self.free_play
        return f"Free play {'enabled' if self.free_play else 'disabled'}."

    def song_finished(self):
        self.queue.advance()
    
    def show_queue(self) -> str:
        if self.queue.is_idle:
            return "Nothing is playing."
        lines = [f"Now playing: {self.queue.now_playing.title}"]
        queued = self.queue.list_queue()
        if not queued:
            lines.append("No songs queued.")
        else:
            lines.append("Up next:")
            for i, song in enumerate(queued, start=1):
                lines.append(f"  {i}) {song.title}")
        return "\n".join(lines)