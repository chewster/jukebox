
from functions.users import checkUsername
from functions.song_queue import *

print("Welcome to the Jukebox!")

username = input("Enter your username: ")
checkUsername(username)
checkQueue = checkQueue()

if not checkQueue: 
    print("The song queue is currently empty. Please add songs to the queue to start playing music.")


addSong = input("Would you like to add a song to the queue? (yes/no) ")
if addSong.lower() == "yes":
    checkSong()
        # Here you would add functionality to allow the user to select an album and add songs to the queue.