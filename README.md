# Jukebox

A command-line jukebox application built in Python as part of a technical assessment.

## Running the app
```bash
python main.py
```

## Running the tests
```bash
python -m pytest tests/
```

## Architecture

The application is split into single-responsibility modules:

- **`models.py`** — `Song` and `Album` dataclasses, pure data with no logic
- **`library.py`** — owns the catalog and handles parsing of 5-character song IDs (e.g. `01-04`)
- **`credits.py`** — credit purchasing logic using a greedy denomination algorithm
- **`queue.py`** — play queue backed by `collections.deque`, tracks current and upcoming songs
- **`jukebox.py`** — thin orchestrator that wires the above together; contains no business logic itself
- **`data/loader.py`** — loads `albums.json` and assigns positional IDs at runtime

The key design principle is that `Jukebox` delegates everything — it never does the work itself. This makes each component independently testable and easy to swap out or extend.

ID parsing lives in `Library` rather than `Jukebox` because it's a catalog concern. The credit denomination logic uses a greedy loop over `[(5, 18), (2, 7), (1, 3)]`, which correctly handles any positive dollar amount (e.g. $8 → $5 + $2 + $1 = 28 credits).

## Stretch goals

Both optional features are implemented:

- **Free play mode** — toggled via the operator menu option, bypasses the credit system entirely
- **Queue removal** — users can remove any queued song by position, with the currently playing song protected from removal
