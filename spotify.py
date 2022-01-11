from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_list_of_recent_tracks(time_in_seconds: int, playlist: str) -> list:
  """
  Returns a list of dicts of posted tracks in a spotify playlist for given timeframe
  :params time_in_seconds: int - Time is seconds that will be used to check for songs from now
  :params playlist: str - Spotify playlist_id to check for added songs
  """

  auth_manager = SpotifyClientCredentials()
  sp = spotipy.Spotify(auth_manager=auth_manager)
  now = datetime.now()
  results = sp.playlist_tracks(playlist)
  tracks = results['items']
  
  # Keys for track dict
  keys = ['User', 'User ID', 'Playlist', 'Playlist ID', 
          'Added Date', 'Artist', 'Track', 'Album', 
          'Release Date', 'Album Art URL', 'Track URL', 'Track ID']
  
  # Cycle through pages to add all songs from pages to tracks
  while results['next']:
      results = sp.next(results)
      tracks.extend(results['items'])

  # Build up relevant data 
  posted_songs = [dict(zip(keys, [sp.user(track['added_by']['id'])['display_name'], # User name 
                  track['added_by']['id'], # User ID
                  sp.playlist(playlist_id=playlist, fields="name")['name'], # Playlist name
                  playlist, # Playlist ID
                  track['added_at'], # Added date
                  track["track"]["album"]["artists"][0]["name"], # Artist
                  track["track"]["name"], # Track title
                  track["track"]["album"]['name'], # Album
                  track["track"]["album"]['release_date'], # Release date 
                  track['track']['album']['images'][0]['url'], # Album art URL
                  track['track']['external_urls']['spotify'],  # Track URL
                  track['track']['id']])) # Track ID
                  for track in tracks if 
                  (now - datetime.strptime(track['added_at'], "%Y-%m-%dT%H:%M:%SZ")).total_seconds() < time_in_seconds]

  return posted_songs
