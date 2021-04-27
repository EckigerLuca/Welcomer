import os
from attr import __description__, __title__
import discord
from discord import file
from discord.client import Client
from discord.ext import commands
import logging

token = 'your token here'

logging.basicConfig(level=logging.INFO)

defaultcolor = discord.Colour.from_rgb(239, 164, 176)

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents.all()

client = commands.Bot(command_prefix='&', intents = intents)

client.remove_command('help')

#bot is ready
@client.event
async def on_ready():
    print("\nI'm ready!11!!!!1!\n")

    game = discord.Game('with some new peoples...')
    await client.change_presence(status=discord.Status.online, activity=game)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename !="__init__.py":
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)