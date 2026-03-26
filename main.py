from data.loader import load_library
from song_queue import checkQueue
from jukebox import Jukebox


def main():
    library = load_library()
    jukebox = Jukebox(library)
    print("\n" + "=" * 40)
    print("         🎵  WELCOME TO THE JUKEBOX  🎵")
    print("=" * 40)
    while True:
        print_menu(jukebox.credits.balance, jukebox.free_play)

        cmd = input("Choose an option: ").strip().lower()

        if cmd == "1":
            print()
            print(jukebox.list_catalog())

        elif cmd == "2":
            raw = input("Enter dollar amount: $").strip()
            if not raw.isdigit() or int(raw) <= 0:
                print("Please enter a positive whole number.")
            else:
                print(jukebox.insert_money(int(raw)))

        elif cmd == "3":
            if jukebox.credits.balance <= 0 and not jukebox.free_play:
                print("Please insert money first.")
                continue
            sel = input("Enter song ID (e.g. 01-04): ").strip()
            print(jukebox.select_song(sel))

        elif cmd == "4":
            print(jukebox.now_playing())

        elif cmd == "5":
            print(jukebox.up_next())

        elif cmd == "6":
            jukebox.song_finished()
            print("Song ended.")
            print(jukebox.now_playing())

        elif cmd == "7":
            print(jukebox.toggle_free_play())

        elif cmd == "8":
            queue_list = list(jukebox.queue._queue)
            if not queue_list:
                print("No songs queued (can't remove the currently playing song).")
            else:
                print("\nQueued songs:")
                for i, song in enumerate(queue_list):
                    print(f"  {i + 1}) {song.title}")
                raw = input("Remove which song? (number): ").strip()
                if raw.isdigit() and 1 <= int(raw) <= len(queue_list):
                    removed = jukebox.queue.remove(int(raw) - 1)
                    print(f"Removed: {removed.title}")
                else:
                    print("Invalid selection.")
        elif cmd == "9":
            print(jukebox.show_queue())

        elif cmd == "q":
            print("\nGoodbye! 🎵")
            break

        else:
            print("Unknown option, try again.")

def print_menu(credits: int, free_play: bool):
    status = "FREE PLAY" if free_play else f"{credits} credit(s)"
    print(f"\n[{status}]")
    print("  1) List catalog")
    print("  2) Insert money")
    print("  3) Select song")
    print("  4) Now playing")
    print("  5) Up next")
    print("  6) Song finished (advance queue)")
    print("  7) Toggle free play  [operator]")
    print("  8) Remove song from queue")
    print("  9) Show queue")
    print("  q) Quit")
    print("-" * 40)




if __name__ == "__main__":
    main()