# :musical_note:**Downloader spotify song**

### Simple free and unlimited spotify playlist downloads 

## Instruction:

1. :open_file_folder: Install the packages required by the application using ```pip install -r requirements.txt```

2. :arrow_right: Paste into variable `BEARER_TOKEN `

3. :link: Copy spotify playlist link and paste into variable `playlist_url`
4. :running: And run the code `python spotify_download.py` (who has Unix/macOs try `python3 spotify_download.py`)
5. :tada: Enjoy the program

---

## :exclamation: **Warning**: 
After each reload of the page, the token changes and you need to insert it again.


## :bell: TODO

- [ ] Automatic token insertion

## :heavy_check_mark: How does it work?

1. We first search the playlist and download a list of songs.
2. We then look up each song on Youtube, download it as an mp4, then convert it to an mp3 and store it in a folder!
