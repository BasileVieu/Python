import discord
from discord.ext import commands


def get_channel(guild: discord.Guild, name: str) :
    for channel in guild.text_channels :
        if channel.name == name :
            return channel

    return None


def in_channel(name: str) :
    def check_in_channel(ctx) :
        return ctx.message.channel.id == get_channel(ctx.guild, name).id

    return commands.check(check_in_channel)
