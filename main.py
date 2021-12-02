import discord
from discord.ext import commands
import asyncio
from discord.ext import tasks
import requests
import time
from datetime import datetime
import pytz

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

async def detectoffline():
  await client.wait_until_ready()
  # Put channel id here
  botid=''
  # Put time zone here
  yourtimezone='America/New_York'
  # Put your discord id here
  userid=123
  channel=client.get_channel(id=botid)
  firstDetect=True
  while not client.is_closed():
    data = requests.get(
      url = "https://api.hypixel.net/player",
      params = {
          # Put api key here
          "key": "",
          # Put minecraft uuid here
          "uuid": "",
      }
    ).json()

    data=data.get("player", {})

    lastLogout=data['lastLogout']
    lastLogin=data['lastLogin']
    displayname=data['displayname']
    tz_NY = pytz.timezone(yourtimezone) 
    datetime_NY = datetime.now(tz_NY)
    current_time=datetime_NY.strftime("%H:%M")

    if lastLogin>lastLogout:
      firstDetect=True
    elif lastLogin<lastLogout:
      if firstDetect:
        embed=discord.Embed(title='Detected Offline', description=f'[{current_time}] {displayname} is offline', color=discord.Colour.red())
        await channel.send(f'<@{userid}>', embed=embed)
        firstDetect=False
      else:
        pass
    await asyncio.sleep(60)

# Put bot token here
bottoken=''

client.loop.create_task(detectoffline())
client.run(bottoken)

