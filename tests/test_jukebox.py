import pytest
from models import Song, Album
from library import Library
from credits import CreditSystem
from play_queue import PlayQueue
from jukebox import Jukebox

# --- Fixtures ---

def make_library():
    albums = [
        Album("01", "Abbey Road", [
            Song("01", "Come Together"),
            Song("02", "Something"),
            Song("03", "Here Comes the Sun"),
        ]),
        Album("02", "Rumours", [
            Song("01", "Go Your Own Way"),
            Song("02", "The Chain"),
        ]),
    ]
    return Library(albums)

# --- Credit tests ---

def test_purchase_1_dollar():
    cs = CreditSystem()
    assert cs.purchase(1) == 3

def test_purchase_2_dollars():
    cs = CreditSystem()
    assert cs.purchase(2) == 7

def test_purchase_5_dollars():
    cs = CreditSystem()
    assert cs.purchase(5) == 18

def test_purchase_8_dollars():
    cs = CreditSystem()
    assert cs.purchase(8) == 28  # 5+2+1

def test_purchase_10_dollars():
    cs = CreditSystem()
    assert cs.purchase(10) == 36  # 5+5

def test_spend_sufficient():
    cs = CreditSystem()
    cs.purchase(1)
    assert cs.spend() is True
    assert cs.balance == 2

def test_spend_insufficient():
    cs = CreditSystem()
    assert cs.spend() is False

# --- Library tests ---

def test_valid_song_lookup():
    lib = make_library()
    song = lib.get_song("01-02")
    assert song.title == "Something"

def test_invalid_album():
    lib = make_library()
    assert lib.get_song("99-01") is None

def test_invalid_song_in_valid_album():
    lib = make_library()
    assert lib.get_song("01-99") is None

def test_malformed_id():
    lib = make_library()
    assert lib.get_song("1-1") is None
    assert lib.get_song("abc") is None
    assert lib.get_song("01_02") is None

# --- Queue tests ---

def test_queue_idle_when_empty():
    q = PlayQueue()
    assert q.is_idle is True
    assert q.now_playing is None
    assert q.up_next is None

def test_first_song_plays_immediately():
    q = PlayQueue()
    q.enqueue(Song("01", "Come Together"))
    assert q.now_playing.title == "Come Together"

def test_second_song_is_up_next():
    q = PlayQueue()
    q.enqueue(Song("01", "Come Together"))
    q.enqueue(Song("02", "Something"))
    assert q.up_next.title == "Something"

def test_advance_queue():
    q = PlayQueue()
    q.enqueue(Song("01", "Come Together"))
    q.enqueue(Song("02", "Something"))
    q.advance()
    assert q.now_playing.title == "Something"

def test_advance_empty_queue_goes_idle():
    q = PlayQueue()
    q.enqueue(Song("01", "Come Together"))
    q.advance()
    assert q.is_idle

# --- Jukebox integration tests ---

def test_select_song_without_credits():
    jukebox = Jukebox(make_library())
    result = jukebox.select_song("01-01")
    assert "Insufficient" in result

def test_select_valid_song_with_credits():
    jukebox = Jukebox(make_library())
    jukebox.insert_money(1)
    result = jukebox.select_song("01-01")
    assert "Come Together" in result

def test_select_invalid_song():
    jukebox = Jukebox(make_library())
    jukebox.insert_money(1)
    result = jukebox.select_song("99-99")
    assert "Error" in result

def test_free_play_bypasses_credits():
    jukebox = Jukebox(make_library())
    jukebox.toggle_free_play()
    result = jukebox.select_song("01-01")
    assert "Come Together" in result