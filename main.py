import discord
# import os
# import random
# import json
# import requests
# import time
import config

from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
from discord.utils import get
from io import BytesIO

# from dotenv import load_dotenv

intents = discord.Intents.all()
# intents.members = True
bot = commands.Bot(command_prefix="!=", guild_subscriptions=True, intents=intents, owner_ids= config.OWNER_ID)

@bot.event
async def on_ready():
    print('Bot: {0.user} is ready'.format(bot))
    activity = discord.Streaming(
        name="!=help for commands, yes its scuffed but oh well, WIP", game="I'm Not Confused",
        url='https://www.twitch.tv/the_gnarwhal', platform = 'Twitch')  # can be any activity,(streaming,game,activity)
    status = discord.Status.online
    await bot.change_presence(activity=activity, status=status)


bot.load_extension("fun")
bot.load_extension("management")
bot.load_extension("listener")
bot.load_extension("randomwalk")

bot.run(config.TOKEN)
