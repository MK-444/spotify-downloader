from youtube_search import YoutubeSearch
from moviepy.editor import *
from pytube import Playlist
import moviepy.editor as mp
from pytube import YouTube
from pathlib import Path
import requests
import json
import re
import os
from requests.structures import CaseInsensitiveDict


global BEARER_TOKEN, playlist_url
BEARER_TOKEN = "<your bearer token>"
playlist_url = '<your playlist>'


def get_new_token():
    url = playlist_url
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    response = requests.get(url, headers=headers)
    return response


def get_tracks(playlist_id, offset, limit, token):
    url = "https://api.spotify.com/v1/playlists/" + str(playlist_id) + "/tracks?offset=" + str(offset) + "&limit=" + str(limit) + "&market=GB"
    payload={}
    headers = {
        'authorization': 'Bearer ' + str(token),
        'Sec-Fetch-Dest': 'empty',
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)


def get_song_names(playlist_id):
    done = False
    offset_counter = 0
    tracks = []
    while not done:
        new_token = get_new_token()
        data = get_tracks(playlist_id, offset_counter, 100, new_token)
        if(not 'total' in data):
            print(data)
            exit()
        if(data['total'] > 0):
            limit = data['limit']
            offset = data['offset']
            total = data['total']
            print('Loading songs from Spotfiy [Limit-' + str(limit) + ',offset-' + str(offset) +',total-' + str(total) +  ']')
            if(offset < total):
                offset_counter += limit
            else:
                print('Done!')
                done = True
            for song in data['items']:
                song_name = song['track']['name']
                artist_name = song['track']['artists'][0]['name']
                print(song_name + ' - ' + artist_name)
                tracks.append({'name' : song_name, 'artist' : artist_name})
        else:
            print('Oh no, playlist is empty :(')
            done = True
    return tracks


def download_playlist(spotify_playlist_id):
    songs = get_song_names(spotify_playlist_id)
    Path('mp3').mkdir(exist_ok=True)
    for song in songs:
        song_name = song['name']
        artist = song['artist']
        search_query = song_name + ' ' + artist
        item_location = 'mp3' +'/'+   ((search_query + '.mp3').replace('"', '').replace("'", '').replace('\\', '').replace('/', ''))
        out_file_error = ''
        if(os.path.isfile(item_location)):
            print(search_query)
            print('\nAlready exists! Skipping!\n')
        else:
            try:
                results = YoutubeSearch(search_query, max_results=1).to_json()
                result = json.loads(results)['videos'][0]
                youtube_id = result['id']
                title = result['title']
                count = result['views']
                print('\n\n====\nDownloading...')
                url = "https://www.youtube.com/watch?v=" + youtube_id
                print(url)
                youtube_url = YouTube(url)
                video = youtube_url.streams.get_highest_resolution()
                out_file = video.download(output_path='temp')
                out_file_error = out_file
                clip = mp.VideoFileClip(out_file)
                clip.audio.write_audiofile(item_location)
            except Exception as e:
                print(e)
                print('Failed to convert ' + str(search_query))
                print('Try doing it manually!')
                f = open('failed_log.txt', 'a')
                f.write(search_query)
                f.close()
        print('====')


regex = re.compile(r"\d\w+")
part_url = regex.findall(playlist_url)
id_playlist = str(part_url)[2:-2]
download_playlist(id_playlist)

