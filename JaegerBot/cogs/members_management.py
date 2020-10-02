import discord
from discord.ext import commands
from Resources.common import get_channel, in_channel


class MembersManagement(commands.Cog) :
    def __init__(self, client: commands.Bot) :
        self.client = client

    # region Listener on_ready
    @commands.Cog.listener()
    async def on_ready(self) :
        print("members_management is ready.")

    # endregion

    # region Listener on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) :
        role = discord.utils.get(member.guild.roles, name = "Newcomer")

        await member.add_roles(role)

        embed = discord.Embed(colour = discord.Colour.green(),
                              title = "Member Information",
                              description = f"{member.display_name} has joined us.")

        embed.set_author(name = self.client.user.name, icon_url = self.client.user.avatar_url)
        embed.set_thumbnail(url = member.avatar_url)

        await get_channel(member.guild, "events").send(embed = embed)

    # endregion

    # region Listener on_member_remove
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) :
        try :
            await member.guild.fetch_ban(member)
            return
        except discord.NotFound :
            embed = discord.Embed(colour = discord.Colour.orange(),
                                  title = "Member Information",
                                  description = f"{member.display_name} has left us.")

            embed.set_author(name = self.client.user.name, icon_url = self.client.user.avatar_url)
            embed.set_thumbnail(url = member.avatar_url)

            await get_channel(member.guild, "events").send(embed = embed)

    # endregion

    # region Listener on_member_ban
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member) :
        embed = discord.Embed(colour = discord.Colour.red(),
                              title = "Member Information",
                              description = f"{member.display_name} has been banned.")

        embed.set_author(name = self.client.user.name, icon_url = self.client.user.avatar_url)
        embed.set_thumbnail(url = member.avatar_url)

        await get_channel(member.guild, "ban").send(embed = embed)

    # endregion

    # region Command Kick
    # --Command--
    @commands.command(name = "kick")
    @in_channel("kick")
    async def kick_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = None) :
        await member.kick(reason = reason)

        channel = get_channel(ctx.guild, "kick")
        await channel.send(f"{member.display_name} has been kicked by {ctx.author.display_name}.")

        if reason is not None :
            await channel.send(f"Reason : {reason}")

    # --Error--
    @kick_command.error
    async def kick_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure) :
            await ctx.send("You can use this command only in \"kick\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please, specify the member you want to kick.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I don't know this member.")

    # endregion

    # region Command Ban
    # --Command--
    @commands.command(name = "ban")
    @in_channel("ban")
    async def ban_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = None) :
        await member.ban(reason = reason)

        channel = get_channel(ctx.guild, "ban")
        await channel.send(f"{member.display_name} has been banned by {ctx.author.display_name}.")

        if reason is not None :
            await channel.send(f"Reason : {reason}")

    # --Error--
    @ban_command.error
    async def ban_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure) :
            await ctx.send("You can use this command only in \"ban\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please, specify the member you want to ban.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I don't know this member.")

    # endregion

    # region Command Unban
    # --Command--
    @commands.command(name = "unban")
    @in_channel("ban")
    async def unban_command(self, ctx: commands.Context, *, member: discord.Member) :
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users :
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator) :
                await ctx.guild.unban(user)
                await get_channel(ctx.guild, "ban").send(f"{user.mention} has been unbanned by {ctx.author.display_name}")
                return

    # --Error--
    @unban_command.error
    async def unban_command_error(self, ctx: commands.Context, error) :
        if isinstance(error, commands.CheckFailure) :
            await ctx.send("You can use this command only in \"ban\" channel.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please, specify the member you want to unban.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I don't know this member.")

    # endregion


def setup(client) :
    client.add_cog(MembersManagement(client))
