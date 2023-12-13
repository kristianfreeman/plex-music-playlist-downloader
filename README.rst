# Plex Music Playlist Downloader (and post-processor)

This is a modified script ([thanks, Chris!](https://github.com/ChrisSn0w/plex-music-playlist-downloader)) for downloading a given playlist from Plex, and post-processing it.

The use-case for this is to backup or prepare a USB drive, SD card, or whatever else as a portable version of your Plex-stored music library for use in a car, etc.

## Installation

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Prepare a `.env` file with the following variables:

```bash
cp .env.example .env
```

- `PLEX_URL` - URL of your Plex server, including port. e.g. `http://localhost:32400`
- `PLEX_TOKEN` - Your Plex API token. See [this guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) to find it.
- `PLEX_PLAYLIST_ID` - The ID of the playlist to download. You can find this by navigating to a playlist in the Plex UI and looking at the URL. The query params in the URL should look like `?key=%2Fplaylists%2F15252` -- the decoded value of this is `?key=/playlists/15252`, so the playlist ID is `15252`.
- `DOWNLOAD_LOCATION` - optionally, download to a different location than the script directory. e.g. "~/Music"
- `POST_PROCESS` - optionally, run a post-processing script after downloading. See below for more info. The format is `<script>`, where the value matches a file `/post_process/{script}.sh`.
- `METADATA_PROCESS` - optionally, specify a path to a metadata script to use for post-processing. See below for more info. The format is `<script>`, where the value matches a file `/metadata_process/{script}.sh`.

3. Running the script

```bash
python dl_plex_playlist.py
```

4. Post-processing and metadata

The script has the ability to run two types of post-download scripts:

- Post-processing, which runs after the playlist files are downloaded. You can use this to convert FLAC to mp3, for instance.
- Metadata, which runs after post-processing. You can use this to rename files or tag them.

Post-processing and metadata scripts are defined in the respective folders in the repo. You can use the example scripts as a starting point. Note that I've written these scripts for my own use-case, so feel free to modify them as needed.

---

original README:

```
**Plex Music Playlist Downloader**

A Python script to download music files from Plex playlists to a local drive or USB thumb drive.

THe audio system in my car plays mp3 and other audio files from a USB thumb drive. This simple script utilizes the python api wrapper written by pkkid  https://github.com/pkkid/python-plexapi to download mp3/audio files from all audio playlists in Plex. Folders with the name of each playlist are created in the current directory and the audio filed are stored in those folders.

*Note:* This is a python 3 script. 

Run it in the directory where the scriot is stored (and where you want the music to be downloaded) with the following command: python3 dl_plex_playlist.py

*Enjoy,*

Chris Snow
```
