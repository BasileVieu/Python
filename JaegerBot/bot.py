import discord
import os
import json
from discord.ext import commands


def get_prefix(temp_client, message: discord.Message) :
    with open("prefixes.json", "r") as f :
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix)


@client.event
async def on_ready() :
    print("Bot is ready.")


for filename in os.listdir("./cogs") :
    if filename.endswith(".py") :
        client.load_extension(f"cogs.{filename[:-3]}")

client.run('NzU0MzM0OTA4MjAxMTczMDkz.X1zPIA.xVfpXPLYq_oTW1tW9wnflcaBldo')
