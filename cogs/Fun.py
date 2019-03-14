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
from datetime import datetime
from PIL import Image,ImageDraw
from discord.ext import commands
from urllib.request import urlopen, Request
from aiohttp import ClientSession

header = {"User-Agent" : "Magic Browser"}
heart = '<a:loading_heart:542883297600995349>'
staff = {'Admin':553314578528993311,
        'Mod':553356112636936203}
muted = 553358001550131208

#lastfm
API_KEY = config.API_KEY  # this is a sample key
API_SECRET = config.API_SECRET

lastfm_network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

class Fun:
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
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def iam(self, ctx):
        await ctx.send(f"{ctx.message.author.mention} is {random.choice(['an edgy', 'a depressed','a dumbass'])} {random.choice(['bitch', 'thot','bastard'])}!")

    @commands.command()
    async def convert(self, ctx, temp: float):
        '''Convert Farenheit to Celsius'''
        C = round((temp-32)/1.8,2)
        await ctx.send(f"{temp}°F is {C}°C")

    @commands.command()
    async def define(self, ctx, *, word: str):
        '''Provide definiton from Google'''
        loading_message = await ctx.send(f"{heart} Now loading... {heart}")
        word = word.replace(' ', '_')
        req = Request(url=f"https://googledictionaryapi.eu-gb.mybluemix.net/?define={word}&lang=en")
        with urlopen(req) as res:
            definition = json.loads(res.read())[0]["meaning"]
        def_embed = discord.Embed(title=word.title(), color=discord.Color.gold())
        for part, part_def in definition.items():
            def_embed.add_field(name=f"*{part}*", value=part_def[0]["definition"])
        await loading_message.edit(content="",embed=def_embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def despacito(self, ctx):
        '''Broken! Don't use.'''
        async for message in ctx.history(limit=2, reverse=True):
            for emoji in '["🇩","🇪","🇸","🇵","🇦","🇨","🇮","🇹"," 🇴"]' :
                await message.add_reaction(emoji)
            break
        try: await ctx.message.delete()
        except: pass

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ping(self, ctx):
        '''Return ping'''
        start = time.time()
        message = await ctx.send(f"My ping is...")
        end = time.time()
        await message.edit(content=f"My ping is... {round((end-start)*1000, 2)} milliseconds.")

    @commands.command()
    async def palette(self, ctx, color_count: int = 5):
        '''Generate a color palette (default 5 colors) based on an image'''
        loading_message = await ctx.send(f"{heart} Now loading... {heart}")
        try:
            attachment = await self.prev_attachedimg(ctx)
            if attachment.size > 3000000:
                await loading_message.delete()
                raise commands.CommandError('Image cannot be more than 3MB.')
            async with ClientSession() as session, session.get(attachment.url) as res:
                image = io.BytesIO(await res.read())
            colors = colorgram.extract(image, color_count)
            imnew = Image.new('RGB',(100*color_count,100))
            imdraw = ImageDraw.Draw(imnew)
            for i, color in enumerate(colors):
                imdraw.rectangle([(i*100, 0), ((i+1)*100, 100)],fill=color.rgb)
            palette = io.BytesIO()
            imnew.save(palette, format='PNG')
            await ctx.send(file=discord.File(palette.getvalue(), 'palette.png'))
        except IOError:
            raise commands.CommandError("The file must be an image.")
        finally:
            await loading_message.delete()

    @commands.command()
    async def lastfm(self, ctx, username: str):
        ''' Look up Last.fm profile'''
        loading_message = await ctx.send(f"{heart} Now loading... {heart}")
        try:
            user = lastfm_network.get_user(username)
            user_embed = discord.Embed(color=discord.Color.red())
            icon = user.get_image()
            user_embed.set_author(name=user.name, url=f"https://www.last.fm/user/{user.name}").set_thumbnail(url=icon if icon else "https://lastfm-img2.akamaized.net/i/u/avatar170s/818148bf682d429dc215c1705eb27b98")
            top_albums_str = "\n".join(str(top_album.item) for top_album in user.get_top_albums()[:3])
            user_embed.add_field(name="Top Albums", value=top_albums_str if top_albums_str else "Nothing found")
            top_artists_str = "\n".join(str(top_artist.item) for top_artist in user.get_top_artists()[:3])
            user_embed.add_field(name="Top Artists",value=top_artists_str if top_artists_str else "Nothing found")
            top_tracks = [track.item for track in user.get_top_tracks()][:3]
            top_tracks_str = "\n".join(f"{top_track.title} - {top_track.artist}" for top_track in top_tracks)
            user_embed.add_field(name="Top Track",value=top_tracks_str if top_tracks_str else "Nothing found")
            await ctx.send(content="",embed=user_embed)
        finally:
            await loading_message.delete()

    @commands.command()
    async def owo(self, ctx, *args):
    	'''Return an owo'd sentence'''
    	sentence = " ".join(args)
    	faces = ["(・`ω´・)", ";;w;;", "owo", "UwU", ">w<", "^w^"]
    	sentence = re.sub(r'[rl]',r'w',sentence)
    	sentence = re.sub(r'[RL]',r'W',sentence)
    	sentence = re.sub(r'([Nn])([AIEOUaieou])',r'\1y\2',sentence)
    	sentence = re.sub(r'(ove)','uv',sentence)
    	sentence = re.sub(r'!+', f" {random.choice(faces)}",sentence)
    	await ctx.send(sentence)

    @commands.command()
    async def mock(self, ctx, *,sentence):
        '''Return a mocking sentence'''
        new_sentence = ''.join(c.lower() if random.randrange(2) else c.upper() for c in sentence)
        await ctx.send(new_sentence)

    @commands.command()
    async def say(self, ctx, *,args):
        '''Make the bot say something'''
        await ctx.message.delete()
        await ctx.send(args)

    @commands.command()
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def fact(self, ctx):
        '''Provide a random fact'''
        with urlopen(Request('http://mentalfloss.com/api/facts')) as res:
            fact = random.choice(json.loads(res.read()))['fact']
        await ctx.send(fact)

    #consider adding a duration bar
    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx, member: discord.Member = None):
        '''Display Spotify now playing status for whoever called the command'''
        member = member if member else ctx.author
        if not isinstance(ctx.message.author.activity, discord.Spotify):
            raise commands.CommandError('You need to be playing a song on Spotify.')
        spotify = member.activity
        duration, current = spotify.duration, datetime.utcnow() - spotify.start
        position = f"{current.seconds//60:02}:{current.seconds%60:02} / {duration.seconds//60:02}:{duration.seconds%60:02}"
        spotify_embed = discord.Embed(title = spotify.title, color =discord.Color.green())
        spotify_embed.add_field(name = "Artist", value = spotify.artist)
        spotify_embed.add_field(name = "Album", value = spotify.album)
        spotify_embed.add_field(name = "Duration", value = position)
        spotify_embed.set_thumbnail(url = spotify.album_cover_url)
        await ctx.send(embed=spotify_embed)

    @commands.command()
    async def e(self, ctx, emote: discord.PartialEmoji):
        async with ClientSession() as session, session.get(emote.url) as res:
            '''Return a full sized emote'''
            image = io.BytesIO(await res.read())
            ext = imghdr.what(image)
            await ctx.send(file=discord.File(image, f'{emote.name}.{ext}'))

def setup(bot):
    bot.add_cog(Fun(bot))
