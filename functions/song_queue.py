import json
from functions.albums import getAlbums

def checkQueue():
    try: 
        with open("data/song_queue.json", "r") as file:
            queue = json.load(file)

            if queue.get('q') is None or len(queue['q']) == 0:
                print("The song queue is currently empty.")
                return False
            else:
                print("Current song queue:")
                for index, song in enumerate(queue['q']):
                    print(f"{index + 1}. {song['title']} by {song['artist']}")
    except json.JSONDecodeError:
        print("Error: 2ue.json is not a valid JSON file.")

def getAlbums():
    try: 
        with open("data/albums.json", "r") as file:
            albums = json.load(file)
            print("Available albums:")
            for index, album in enumerate(albums['albums']):
                print(f"{index + 1}. {album['title']} by {album['artist']}")
                for song_index, song in enumerate(album['songs']):
                    print(f"   - {song_index}.  {song['title']} ({song['duration']})")
    except json.JSONDecodeError:
        print("Error: albums.json is not a valid JSON file.")

def addSong(song, artist, duration):
    try: 
        with open("data/song_queue.json", "r+") as file:
            queue_data = json.load(file)
            song_entry = {"title": song, "artist": artist, "duration": duration}
            queue_data['q'].append(song_entry)
            file.seek(0)
            json.dump(queue_data, file)
    except json.JSONDecodeError:
        print("Error: albums.json is not a valid JSON file.")


def checkSong(): 
    print("here are the list of available songs you can add to the queue:")
    getAlbums()
    album_num = int(input("Enter the number of the album you want to select: "))
    song_num = int(input("Enter the number of the song you want to add to the queue: "))
    try: 
        with open("data/albums.json", "r") as file:
            albums = json.load(file)
            selected_album = albums['albums'][album_num - 1]
            selected_song = selected_album['songs'][song_num - 1]
            addSong(selected_song['title'], selected_album['artist'], selected_song['duration'])
            # Here you would add functionality to add the selected song to the queue.
    except json.JSONDecodeError:
        print("Error: albums.json is not a valid JSON file.")
    except IndexError:
        print("Invalid album or song number. Please try again.")
        addSongInput = input("Would you like to try adding a song again? (yes/no) ")
        if addSongInput.lower() == "yes":
            checkSong()
