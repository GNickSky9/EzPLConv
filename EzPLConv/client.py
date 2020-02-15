import spotipy
import os
import sys
import googleapiclient.discovery
import json
import urllib
import argparse
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Shows the artist, name, and duration of each song
def showTracks(playlist,file):
    for item in playlist['items']:
        track = item['track']
        file.write(track['artists'][0]['name'] + ' - ' + track['name'] \
            + ' - ' + str(track['duration_ms']) + "\n")

# Gets tracks from a playlist and stores it
def getTracks(playlistID,file):
    clientCredentialsManager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=clientCredentialsManager)

    playlist = sp.playlist(playlistID, fields="tracks,next")
    tracks = playlist['tracks']
    showTracks(tracks, file)
    while tracks['next']:
        tracks = sp.next(tracks)
        showTracks(tracks, file)

# Returns a list of tuples of songs separated by artist, song name, duration
def buildQueue(file):
    queue = []
    for song in file:
        temp = [x.strip() for x in song.split('-')]
        queue.append(tuple(temp))
    return queue

# Heuristic to determine which video is most fitting for selection
def bestVideoHeuristic(song,videoUrls,videoDurations,videoTitles=None):
    artist = song[0]
    songName = song[1]
    duration = song[2]
    keyWords = ['acoustic','Acoustic','live','Live','remix','Remix']
    newDurations = []
    result = None

    # Convert youtube duration format to seconds
    for i in range(len(videoDurations)):
        sum = 0
        temp = videoDurations[i]
        for j in range(len(temp)):
            if temp[j] == 'M':
                sum = sum + (int(temp[j-1])*60)
                if temp[j-2] == 'T':
                    pass
                else:
                    sum = sum + ((int(temp[j-2]*60))*10)
            if temp[j] == 'S':
                sum = sum + int(temp[j-1])
                if temp[j-2] == 'M':
                    pass
                else:
                    sum = sum + (int(temp[j-2]) * 10)
        newDurations.append(sum)

    cnt = 0
    for i in newDurations:
        if int(i) == (int(song[2])/1000):
            result = videoUrls[cnt]
            break
        elif int(i) > (int(song[2])/1000) or int(i) < (int(song[2])/1000):
            x = int(i) - (int(song[2])/1000)
            if abs(x) < 2:
                result = videoUrls[cnt]
                break
        cnt += 1

    return 'https://www.youtube.com/watch?v='+result


# Get the urls to the best videos corresponding to the songs desired
def getUrls(queue):
    try:
        DEVELOPER_KEY = os.environ['YOUTUBE_API_ID']
    except KeyError:
        print("Please Set Environment Variable: 'YOUTUBE_API_ID'")

    goodUrls = []
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    try:
        for song in queue:
            searchResults = youtube.search().list(q=song[0]+' '+song[1], \
                type='video',part='id',maxResults=5).execute() # 1 quota unit
            """
                searchResults contains a map with a key "items" that contains
                a list of maps with keys "id" that contain a map with a key
                "videoId".
            """
            items = searchResults.get('items',[])
            vidUrls = []
            for item in items:
                vidUrls.append(item["id"]["videoId"])

            durations = []
            for url in vidUrls:
                searchURL = 'https://www.googleapis.com/youtube/v3/videos?id=' \
                    +url+'&part=contentDetails'+'&key='+DEVELOPER_KEY         # 3 quota unit
                response = urllib.request.urlopen(searchURL).read()
                data = json.loads(response)
                all_data = data['items']
                contentDetails = all_data[0]['contentDetails']
                duration = contentDetails['duration']
                durations.append(duration)

            goodUrls.append(bestVideoHeuristic(song,vidUrls,durations))
            output = open('urls.txt','w')
            for url in goodUrls:
                output.write(url+'\n')

    except HttpError as err:
        print("A rate limit error or connection error %d occured\n" \
            % (err.resp.status))


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

    getUrls(queue)



if __name__ == "__main__":
    main()
