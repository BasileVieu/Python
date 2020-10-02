import discord
import json
from discord.ext import commands
from Resources.common import get_channel, in_channel


class BotManagement(commands.Cog) :
    def __init__(self, client: commands.Bot) :
        self.client = client

    # region Listener on_ready
    @commands.Cog.listener()
    async def on_ready(self) :
        await self.client.change_presence(status = discord.Status.online,
                                          activity = discord.Activity(type = discord.ActivityType.watching,
                                                                      name = "type !help for commands"))
        print("bot_management is ready.")

    # endregion

    # region Listener on_command_error
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CommandNotFound) :
            await ctx.send("I don't know this command.")

    # endregion

    # region Command Prefix
    # --Command--
    @commands.command(name = "prefix")
    @in_channel("commands")
    async def change_prefix_command(self, ctx: commands.Context, prefix: str) :
        with open("prefixes.json", "r") as f :
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f :
            json.dump(prefixes, f, indent = 4)

        await ctx.send(f"Prefix change to \"{prefix}\".")

    # --Error--
    @change_prefix_command.error
    async def change_prefix_command_error(self, ctx: commands.Context, error) :
        await ctx.send(type(error))

        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can use this command only in \"commands\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the new prefix.")

    # endregion

    # region Command Ping
    # --Command--
    @commands.command(name = "ping")
    @in_channel("events")
    async def ping_command(self, ctx: commands.Context) :
        await get_channel(ctx.guild, "events").send(f"{round(self.client.latency * 1000)}ms")

    # --Error--
    @ping_command.error
    async def ping_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can use this command only in \"events\" channel.")

    # endregion

    # region Command Load
    # --Command--
    @commands.command(name = "load")
    @in_channel("commands")
    async def load_command(self, ctx: commands.Context, extension: str) :
        self.client.load_extension(f"cogs.{extension}")

        await ctx.send(f"{extension} has just been loaded.")

    # --Error--
    @load_command.error
    async def load_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can use this command only in \"commands\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the name of the cog you want to load.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("This cog is already loaded or doesn't exist.")

    # endregion

    # region Command Unload
    # --Command--
    @commands.command(name = "unload")
    @in_channel("commands")
    async def unload_command(self, ctx: commands.Context, extension: str) :
        self.client.unload_extension(f"cogs.{extension}")
        
        await ctx.send(f"{extension} has just been unloaded.")

    # --Error--
    @unload_command.error
    async def unload_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can use this command only in \"commands\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the name of the cog you want to unload.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("This cog is already unloaded or doesn't exist.")

    # endregion


def setup(client) :
    client.add_cog(BotManagement(client))
