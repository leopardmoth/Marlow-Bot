# import necessary modules
import random
import json
import discord
import asyncio
import time
import pylast
import colorgram
import os
import os.path
import re
import io
import typing
import config
import typing
import imghdr
from PIL import Image,ImageDraw
from discord.ext import commands
from urllib.request import urlopen, Request
from aiohttp import ClientSession

header = {"User-Agent" : "Magic Browser"}
heart = '<a:loading_heart:542883297600995349>'
staff = {'Admin':553314578528993311,
        'Mod':553356112636936203}
muted = 553358001550131208

class Utility:
    def __init__(self,bot):
        self.bot = bot

    async def prev_attachedimg(self, ctx):
        '''Return the latest attached message'''
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
        else:
            attach_msg = await ctx.history().find(lambda m: m.attachments)
            if attach_msg == None: raise commands.CommandError(f"Attachment not found.")
            attachment = attach_msg.attachments[0]
        return attachment

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, members: commands.Greedy[discord.Member], minutes: typing.Optional[int] = 10, *, reason = 'no reason'):
        '''Apply muted role'''
        if not members:
            raise commands.CommandError("Needs user(s).")
        for member in members:
            await member.add_roles(discord.Object(muted),reason = f"{ctx.author.name} gave the reason: {reason}")
        if len(members) == 1:
            await ctx.send(f'{members[0].mention} was muted for {minutes} minute(s) because {reason}.')
            channel = self.self.bot.get_channel(555216652589858816)
            await channel.send(f'{members[0].mention} was muted for {minutes} minute(s) because {reason}.')
        else:
            await ctx.send(f'{", ".join(member.mention for member in members)} were muted for {minutes} minute(s) because {reason}.')
            channel = get_channel(555216652589858816)
            await channel.send(f'{", ".join(member.mention for member in members)} were muted for {minutes} minute(s) because {reason}.')
        await asyncio.sleep(minutes*60)
        for member in members:
            await member.remove_roles(discord.Object(muted))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, members: commands.Greedy[discord.Member]):
        '''Remove muted role'''
        if not members:
            raise commands.CommandError("Needs user(s).")
        for member in members:
            await member.remove_roles(discord.Object(muted))
        if len(members) == 1:
            await ctx.send(f'{members[0].mention} has been unmuted! Behave from now on!')
        else:
            await ctx.send(f'{", ".join(member.mention for member in members)} have been unmuted! Behave from now on!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason = 'no reason'):
        '''Kick member(s)'''
        if not members:
            raise commands.CommandError("Needs user(s).")
        for member in members:
            await member.kick(reason = f"{ctx.author.name} gave the reason: {reason}")
        if len(members) == 1:
            await ctx.send(f'{member.display_name} has been kicked because {reason}.')
            channel = self.bot.get_channel(555216652589858816)
            await channel.send(f'{member.display_name} has been kicked because {reason}.')
        else:
            await ctx.send(f'{", ".join({member.display_name} for member in members)} have been kicked because {reason}.')
            channel = self.bot.get_channel(555216652589858816)
            await channel.send(f'{", ".join({member.display_name} for member in members)} have been kicked because {reason}.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member], *, reason = 'no reason'):
        '''Ban member(s)'''
        if not members:
            raise commands.CommandError("Needs user(s).")
        for member in members:
            await member.ban(reason = f"{ctx.author.name} gave the reason: {reason}")
        if len(members) == 1:
            await ctx.send(f'{member.display_name} has been banned because {reason}.')
            channel = self.bot.get_channel(555216652589858816)
            await channel.send(f'{member.display_name} has been banned because {reason}.')
        else:
            await ctx.send(f'{", ".join({member.display_name} for member in members)} have been banned because {reason}.')
            channel = self.bot.get_channel(555216652589858816)
            await channel.send(f'{", ".join({member.display_name} for member in members)} have been banned because {reason}.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, amount: int):
        '''Prune messages'''
        await ctx.channel.purge(limit = amount +1)
        message = await ctx.send(f"{amount} messages pruned.")
        await asyncio.sleep(4)
        await message.delete()

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emote: typing.Optional[discord.PartialEmoji], name):
        '''Steal an emote from an existing emote or image'''
        if (emote):
                async with ClientSession() as session, session.get(emote.url) as res:
                    image = io.BytesIO(await res.read())
        else:
            attachment = await self.prev_attachedimg(ctx)
            async with ClientSession() as session, session.get(attachment.url) as res:
                image = io.BytesIO(await res.read())
        emote = await ctx.guild.create_custom_emoji(name = name, image = image.getvalue())
        await ctx.send(f"Emoji successfully created! {emote}")

    @commands.command()
    @commands.is_owner()
    async def avatar(self, ctx):
        '''Change avatar of the bot, owner's use only'''
        attachment = await self.prev_attachedimg(ctx)
        async with ClientSession() as session, session.get(attachment.url) as res:
            image = io.BytesIO(await res.read())
            await self.self.bot.user.edit(avatar=image.getvalue())
        await ctx.send(f'My avatar is changed!')

def setup(bot):
    bot.add_cog(Utility(bot))
