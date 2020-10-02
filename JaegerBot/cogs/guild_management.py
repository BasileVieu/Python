import discord
import json
from discord.ext import commands


class GuildManagement(commands.Cog) :
    def __init__(self, client: commands.Bot) :
        self.client = client

    # region Listener on_ready
    @commands.Cog.listener()
    async def on_ready(self) :
        print("guild_management is ready.")

    # endregion

    # region Listener on_guild_join
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) :
        with open("prefixes.json", "r") as f :
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "!"

        with open("prefixes.json", "w") as f :
            json.dump(prefixes, f, indent = 4)

    # endregion

    # region Listener on_guild_remove
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) :
        with open("prefixes.json", "r") as f :
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("prefixes.json", "w") as f :
            json.dump(prefixes, f, indent = 4)

    # endregion


def setup(client) :
    client.add_cog(GuildManagement(client))
