import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

# Shows the artist and song name of each track
def showTracks(playlist,file,sp):
    for item in playlist['items']:
        track = item['track']
        file.write(track['artists'][0]['name'] + ' - ' + track['name'] + ' : ' \
        + str(track['duration_ms']) + '\n')


# Gets tracks from a playlist and stores it
def getTracks(playlistID,file):
    clientCredentialsManager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)

    playlist = sp.playlist(playlistID, fields="tracks,next")
    tracks = playlist['tracks']
    showTracks(tracks, file, sp)
    while tracks['next']:
        tracks = sp.next(tracks)
        showTracks(tracks, file, sp)

# Returns a list of tuples of songs to be downloaded separated by artist + song name
def buildQueue(file):
    queue = []
    for song in file:
        temp = [x.strip() for x in song.split('-')]
        queue.append(tuple(temp))
    return queue

# Heuristic to determine which video is most fitting when searching on youtube
def bestVideoHeuristic():
    return

# Get the urls of the best videos corresponding to songs desired
def getUrls(queue):
    urls = []

    return urls

def main():
    if len(sys.argv) > 1:
        playlistID = sys.argv[1]
    else:
        print("Need Playlist ID!")
        print("usage: python " + sys.argv[0] + " [playlist id]")
        sys.exit()

    output = open("tracks.txt", "w")
    getTracks(playlistID,output)
    output.close()

    songs = open("tracks.txt")
    queue = buildQueue(songs)
    songs.close()

    queueSize = len(queue)





if __name__ == "__main__":
    main()
