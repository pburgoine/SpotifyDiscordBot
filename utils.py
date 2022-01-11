from replit import db
from datetime import datetime
import os
from spotify import get_list_of_recent_tracks

def format_track_data_as_message(track: dict) -> str:
  """
  Creates formatted message ready for posting to Discord
  :params track: dict - dictionary of track information about track to be nicely formatted
  """
  
  message = f"""New track added to **{track['Playlist']}** by **{track['User']}**!
  {track['Artist']}-{track['Track']}
  {track['Album']} ({track['Release Date']})
  {track['Album Art URL']}
  {track['Track URL']}
  """
  return message

def check_track_not_posted_before(track_dict: dict) -> bool:
  """
  Removes entries from the list that have been posted before
  :params track_dict: dict - track dict to be filtered after checking the database
  """
  
  try: 
    db[f"{track_dict['Track ID']}_{track_dict['User ID']}_{track_dict['Playlist ID']}"]
    return True
  except KeyError:
    return False

def update_db_with_track_post(track_dict: dict) -> None:
  """
  Add entry to database after posting track
  :params track_dict: dict - track dict to be added to db
  """
  
  db[f"{track_dict['Track ID']}_{track_dict['User ID']}_{track_dict['Playlist ID']}"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

def clear_db() -> None:
  """
  Clears all entries in db
  """
  for key in db.keys():
    del db[key]

def get_songs() -> None:

  playlists = (os.environ['SPOTIFY_PLAYLIST']).split(',')
  time_in_seconds = 60 * 1440 * 100 # SWAP THIS TO WHATEVER THE FREQUENCY THIS RUNS AT

  # Get all the tracks in the playlist from time period
  tracks = []
  for playlist in playlists:
    tracks.extend(get_list_of_recent_tracks(time_in_seconds, playlist))

  # Make sure track isn't posted before
  tracks = [track for track in tracks if check_track_not_posted_before(track) is False]

  return tracks


