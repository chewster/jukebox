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

## Extending to an HTTP API

While not implemented here, the architecture is designed with a future HTTP API in mind. Each public method on `Jukebox` maps cleanly to an HTTP endpoint:

| Method | Endpoint |
|---|---|
| `list_catalog()` | `GET /catalog` |
| `insert_money()` | `POST /credits` |
| `select_song()` | `POST /queue` |
| `now_playing()` | `GET /now-playing` |
| `show_queue()` | `GET /queue` |
| `remove_song()` | `DELETE /queue/{position}` |

### Supporting multiple simultaneous clients

The interesting challenge is real-time state updates — for example, two clients (a mobile app and a kiosk terminal) both need to see `now_playing` change the moment a song advances.

My approach would be:

**State layer** — move shared state (current song, queue, credit balance) out of the in-process `Jukebox` instance and into a shared store. Redis (AWS ElastiCache) is a natural fit here — the queue maps directly to a Redis list, and reads are fast enough for high-frequency polling.

**Real-time updates** — rather than polling, clients would connect via WebSockets (AWS API Gateway WebSocket API). When a song advances, the server publishes an event to an SNS topic; a Lambda subscriber fans the update out to all connected clients. This is an event-driven pattern that scales horizontally without any client needing to know about the others.

**Concurrency** — `select_song` and `song_finished` are write operations that need to be atomic. In a Lambda environment I'd use a Redis distributed lock (via `redlock`) or a DynamoDB conditional write to prevent race conditions when multiple clients interact simultaneously.

**Deployment sketch:**
```
Client (mobile/kiosk)
    │
    ├── REST calls ──► API Gateway ──► Lambda ──► ElastiCache (queue + credits)
    │
    └── WebSocket ───► API Gateway WebSocket ──► Lambda (connection manager)
                                                      │
                                              SNS topic (song events)
                                                      │
                                              Lambda (fan-out to connections)
```

This keeps the core `Jukebox` logic largely unchanged — the Lambda handlers would be a thin wrapper around the same domain objects, with Redis replacing the in-process deque and credit balance.