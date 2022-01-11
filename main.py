import discord
import os
from discord.ext import tasks, commands
from utils import update_db_with_track_post, get_songs,format_track_data_as_message
from keep_alive import keep_alive

keep_alive()
bot = commands.Bot(command_prefix="!")
# client = discord.Client()

@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")
  get_songs_fn.start()

@tasks.loop(minutes=5)
async def get_songs_fn():
    print("Checking for new songs")
    new_songs = get_songs()
    print(new_songs)
    channel = bot.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))
    for track in new_songs:
        # Formatting track for Discord post
      formatted_track = format_track_data_as_message(track)
      await channel.send(formatted_track)
      update_db_with_track_post(track)

bot.run(os.getenv('DISCORD_TOKEN'))









