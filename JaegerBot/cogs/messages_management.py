import discord
import asyncio
from discord.ext import commands, tasks
from Resources.common import get_channel, in_channel


class MessagesManagement(commands.Cog) :
    def __init__(self, client: commands.Bot) :
        self.client = client

    # region Listener on_ready
    @commands.Cog.listener()
    async def on_ready(self) :
        self.change_status_with_time.start()
        print("messages_management is ready.")

    # endregion

    # region Listener cog_unload
    def cog_unload(self) :
        self.change_status_with_time.cancel()

    # endregion

    # region Listener on_message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) :
        if message.author == self.client.user :
            return

        self.change_status_with_time.restart()

        await self.client.change_presence(status = discord.Status.online,
                                          activity = discord.Activity(type = discord.ActivityType.watching,
                                                                      name = "type !help for commands"))

        if message.content.lower().startswith('hello') :
            await message.channel.send(f'Hello {str(message.author).split("#")[0]}')

    # endregion

    # region Loop change_status_with_time
    @tasks.loop()
    async def change_status_with_time(self) :
        await asyncio.sleep(120)
        await self.client.change_presence(status = discord.Status.idle,
                                          activity = discord.Activity(type = discord.ActivityType.watching,
                                                                      name = "type !help for commands"))

    # endregion

    # region Command Clear
    # --Command--
    @commands.command(name = "clear")
    @in_channel("commands")
    @commands.has_any_role("Owner", "Moderator")
    async def clear_command(self, ctx: commands.Context, amount: int, channel: str) :
        await get_channel(ctx.guild, channel).purge(limit = amount)

    # --Error--
    @clear_command.error
    async def clear_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.MissingAnyRole) :
            await ctx.send("You're not allowed to use this command.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You can use this command only in \"commands\" channel.")
        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument, commands.CommandInvokeError)) :
            await ctx.send("Please specify an amount of messages to delete then the channel to purge.")

    # endregion


def setup(client) :
    client.add_cog(MessagesManagement(client))
