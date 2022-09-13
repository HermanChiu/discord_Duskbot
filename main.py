import discord
import os
import asyncio
# import random
# import json
# import requests
# import time
import config
# from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from discord.utils import get
from io import BytesIO

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!=", guild_subscriptions=True, intents=intents, owner_ids= config.OWNER_ID)#,activity=activity, status=status )

@bot.event
async def on_ready():
    print(f'Bot: {bot.user} is ready')
    activity = discord.Streaming(
        name="!=help for commands, yes its scuffed but oh well, WIP", game="I'm Not Confused",
        url='https://www.twitch.tv/the_gnarwhal', platform = 'Twitch')  # can be any activity,(streaming,game,activity)
    status = discord.Status.online
    await bot.change_presence(activity=activity, status=status)

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(config.TOKEN)

asyncio.run(main())
# bot.load_extension("fun")
# bot.load_extension("management")
# bot.load_extension("listener")
# bot.load_extension("randomwalk")

# client.load_extension("management")

# bot.run(config.TOKEN)

