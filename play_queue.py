from collections import deque
from models import Song
from typing import Optional

class PlayQueue:
    def __init__(self):
        self._current: Optional[Song] = None
        self._queue: deque[Song] = deque()

    def enqueue(self, song: Song):
        if self._current is None:
            self._current = song  # start playing immediately if idle
        else:
            self._queue.append(song)

    def advance(self):
        """Call when current song finishes. Pulls next from queue."""
        self._current = self._queue.popleft() if self._queue else None

    @property
    def now_playing(self) -> Optional[Song]:
        return self._current

    @property
    def up_next(self) -> Optional[Song]:
        return self._queue[0] if self._queue else None

    @property
    def is_idle(self) -> bool:
        return self._current is None

    def remove(self, index: int) -> Optional[Song]:
        """Stretch goal: remove a queued song by position (0 = next up)."""
        queue_list = list(self._queue)
        if index < 0 or index >= len(queue_list):
            return None
        removed = queue_list.pop(index)
        self._queue = deque(queue_list)
        return removed
    
    def list_queue(self) -> list[Song]:
        return list(self._queue)