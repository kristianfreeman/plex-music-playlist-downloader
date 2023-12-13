#! /usr/bin/python3

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from plexapi.server import PlexServer

baseurl = os.getenv('PLEX_URL')
if baseurl is None or baseurl == "":
    print("Error: PLEX_URL not set")
    exit(1)

token = os.getenv('PLEX_TOKEN')
if token is None or token == "":
    print("Error: PLEX_TOKEN not set")
    exit(1)

playlist_to_get = os.getenv('PLEX_PLAYLIST_ID')
if playlist_to_get is None or playlist_to_get == "":
    print("Error: PLEX_PLAYLIST_ID not set")
    exit(1)

download_location = os.getenv('DOWNLOAD_LOCATION')
if download_location:
    # if it's a user directory, expand it
    if download_location.startswith('~'):
        download_location = os.path.expanduser(download_location)

    # if it's a relative path, make it absolute
    if not os.path.isabs(download_location):
        download_location = os.path.abspath(download_location)

    print("Setting download location to " + download_location)

metadata_process = os.getenv('METADATA_PROCESS')
post_process = os.getenv('POST_PROCESS')

plex = PlexServer(baseurl, token)

for playlist in plex.playlists(playlistType='audio'):
    playlistId = str(playlist.ratingKey)

    if playlistId != playlist_to_get:
        continue

    print(f'Processing playlist {playlist.title}')
    playlist_path = Path(download_location + "/" + playlist.title)
    
    tracks = playlist.items()
    for track in range(len(tracks)):
        p = Path(tracks[track].locations[0])
        filepath = playlist.title + "/" + p.name

        if download_location:
            filepath = download_location + "/" + filepath

        path = Path(filepath)

        if path.is_file():
            print(f'File {path} exists - skipping')
        else:
            print(f'Creating {path}')
            tracks[track].download(keep_original_name=True, savepath=playlist_path)

    if post_process:
        print(f'Running post process command {post_process}')
        # get matching shell script from post_process/{post_process}
        # first check it exists
        if not os.path.exists(f'post_process/{post_process}.sh'):
            print(f'Error: post process command {post_process} not found. Create post_process/{post_process}.sh to continue')
            exit(1)
    
        # then run it
        os.system(f'./post_process/{post_process}.sh "{str(playlist_path)}"')

    if metadata_process:
        print(f'Running metadata process command {metadata_process}')
        if not os.path.exists(f'metadata_process/{metadata_process}.sh'):
            print(f'Error: metadata process command {metadata_process} not found. Create metadata_process/{metadata_process}.sh to continue')
            exit(1)
    
        # then run it
        os.system(f'./metadata_process/{metadata_process}.sh "{str(playlist_path)}"')

