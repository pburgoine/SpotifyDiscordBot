- Bot that posts to Discord Channel whenever a new song is added to selected playlist(s).

- Will check for new songs every 5 minutes, creating and posting for each new song added.

- Updates db with posts to avoid double posting the same songs.

- ENV variables required to work: 
  - `DISCORD_TOKEN` - discord bot token
  - `DISCORD_CHANNEL_ID` - discord channel ID for bot to post to (needs to have permission to post there)
  - `SPOTIPY_CLIENT_ID` - client_id for spotify api
  - `SPOTIPY_CLIENT_SECRET` - client_secret for spotify api
  - `SPOTIFY_PLAYLIST` - comma separated list of spotify playlist IDs to monitor