import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys

def showTracks(playlist,file):
    for item in playlist['items']:
        track = item['track']
        file.write(track['artists'][0]['name'] + ' - ' + track['name'] + '\n')
        
def getTracks(playlistID,file):
    clientCredentialsManager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)

    playlist = sp.playlist(playlistID, fields="tracks,next")
    tracks = playlist['tracks']
    showTracks(tracks, file)
    while tracks['next']:
        tracks = sp.next(tracks)
        showTracks(tracks, file)

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


if __name__ == "__main__":
    main()