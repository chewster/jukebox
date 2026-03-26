import json

def getAlbums():
    try: 
        with open("data/albums.json", "r") as file:
            albums = json.load(file)
            print("Available albums:")
            for index, album in enumerate(albums['albums']):
                print(f"{index + 1}. {album['title']} by {album['artist']}")
    except json.JSONDecodeError:
        print("Error: albums.json is not a valid JSON file.")