# import necessary modules
import random
import json
import discord
import time
import pylast
import colorgram
import re
import io
import typing
import config
import imghdr
import lyricsgenius
import urbandictionary as ud
from datetime import datetime
from PIL import Image, ImageDraw
from discord.ext import commands
from urllib.request import urlopen, Request
from aiohttp import ClientSession
from datetime import datetime
from static_data import ddragon

header = {"User-Agent" : "Magic Browser"}
heart = '<a:loading_heart:542883297600995349>'
staff = {'Admin':553314578528993311,
    'Mod':553356112636936203}
muted = 553358001550131208

#lastfm
API_KEY = config.API_KEY  # this is a sample key
API_SECRET = config.API_SECRET

lastfm_network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

class Fun(commands.Cog):
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

  async def google_search(self, query, image=False):
    params = {"q": query, "key": config.G_KEY, "cx": config.G_ID}
    search_url = "https://www.googleapis.com/customsearch/v1"
    if image:
        params["searchType"] = "image"
    async with ClientSession() as session, session.get(search_url, params=params) as result:
        return (await result.json())["items"]

  @commands.command()
  @commands.cooldown(2, 20, commands.BucketType.user)
  async def iam(self, ctx):
    await ctx.send(f"{ctx.message.author.mention} is {random.choice(['an edgy', 'a depressed','a dumbass'])} {random.choice(['bitch', 'thot','bastard'])}!")

  @commands.command()
  async def port(self, ctx, member: discord.Member = None):
    '''port in oublic moment'''
    if member is None:
      await ctx.send(f"WHOT HE HECC POSTED PORT IM IN OUBLCI")
    else:
      await ctx.send(f"WHAT HE HECC {member.mention} POSTED PORT IM IN OUBLCI")
    
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

  @commands.command(aliases=['g', 'search'])
  async def google(self, ctx, *, query):
      search_results = await self.google_search(query)
      google_embed = discord.Embed(
          description="", title="Google Search Results", color=discord.Color.red())
      for i, result in enumerate(search_results[:5], 1):
          google_embed.description += f'{i}. [{result["title"]}]({result["link"]})\n'
      await ctx.send(embed=google_embed)

  @commands.command(aliases=['im', 'img'])
  async def image(self, ctx, *, query):
      search_results = await self.google_search(query, image=True)
      google_embed = discord.Embed(
          description=search_results[0]["title"], title="Google Image Search Results", color=discord.Color.red())
      google_embed.set_image(url=search_results[0]["link"])
      await ctx.send(embed=google_embed)

  @commands.command(aliases=['ud'])
  async def urbandictionary(self, ctx, *, query):
    result = ud.define(query)
    result = result[0]
    ud_embed = discord.Embed(
        title=f"{query}", description=f"{result.definition} \n*{result.example}*", color=discord.Color.blue())
    await ctx.send(embed=ud_embed)

  @commands.command(enabled=False)
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def despacito(self, ctx):
    '''Broken! Don't use.'''
    emoji = '\U0001F44D'
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
      color_list = []
      for i, color in enumerate(colors):
        imdraw.rectangle([(i*100, 0), ((i+1)*100, 100)],fill=color.rgb)
        color_list.append(
            f"{color.rgb.r} {color.rgb.g} {color.rgb.b} #{color.rgb[0]:02x}{color.rgb[1]:02x}{color.rgb[2]:02x}")
        color_str = '\n'.join(map(str,color_list))
      with io.BytesIO() as palette:
        imnew.save(palette, format='PNG')
        palette.seek(0)
        await ctx.send(file=discord.File(fp=palette,filename='palette.png'))
      await ctx.send(f"`{color_str}`")
    except IOError:
      raise commands.CommandError("The file must be an image.")
    finally:
      await loading_message.delete()

  @commands.command(aliases=['fm','last'])
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
    except pylast.WSError:
      raise commands.CommandError("User not found.")
    finally:
      await loading_message.delete()

  @commands.command()
  async def league(self, ctx, username):
    my_region = "na1"
    summoner = config.watcher.summoner.by_name(my_region, username)
    summoner_id = str(summoner['id'])
    champion_info = config.watcher.champion_mastery.by_summoner(my_region, summoner_id)
    dd = ddragon.ddragon()
    champ = []
    champ_lvl = []
    champ_play = []
    for i in range(5):
      champion_info[i]['lastPlayTime'] = datetime.utcfromtimestamp(
          champion_info[i]['lastPlayTime'] / 1000).strftime('%b %d, %Y')
      champion_info[i]['championId'] = dd.getChampion(
          champion_info[i]['championId']).name
      if champion_info[i]['chestGranted'] == "True":
        champion_info[i]['chestGranted'] = "Yes"
      else:
        champion_info[i]['chestGranted'] = "No"
      champ.append(f"{champion_info[i]['championId']}")
      champ_list = '\n'.join(map(str, champ))
      champ_lvl.append(f"{champion_info[i]['championLevel']}")
      champ_level = '\n'.join(map(str, champ_lvl))
      champ_play.append(f"{champion_info[i]['lastPlayTime']}")
      champ_playtime = '\n'.join(map(str, champ_play))
    
    lol_embed = discord.Embed(
          title=f"{username}'s Summoner Stats", color=discord.Color.blue())
    lol_embed.add_field(name="Champion", value=champ_list)
    lol_embed.add_field(name="Champion Level", value=champ_level)
    lol_embed.add_field(name="Last Played", value=champ_playtime)
    lol_embed.set_thumbnail(url=dd.getIcon(
        summoner['profileIconId']).image)
    await ctx.send(embed=lol_embed)

  @commands.command()
  async def owo(self, ctx, *, arg):
    '''Return an owo'd sentence'''
    sentence = arg
    faces = ["(・`ω´・)", "ᕕ( ᐛ )ᕗ", " (灬´ᴗ`灬)", "owo", "uwu", ">w<", "^w^"]
    sentence = re.sub(r"[rl]", r"w", sentence)
    sentence = re.sub(r"[RL]", r"W", sentence)
    sentence = re.sub(r"([Nn])([AIEOUaieou])", r"\1y\2", sentence)
    sentence = re.sub(r"(ove)", "uv", sentence)
    sentence = re.sub(r"!+", f" {random.choice(faces)}", sentence)
    await ctx.send(sentence)
  
  @owo.error
  async def owo_handler(self, ctx,error):
    faces = ["(´；д；)", "(´；ω；`)", "(｡ﾉω＼｡)",
             "(╯︵╰,)", "(´Д｀。", "(´；д；)", "(ᗒᗩᗕ)"]
    if isinstance(error, commands.MissingRequiredArgument):
      if error.param.name == "arg":
        await ctx.send(f"Give me a sentence! {random.choice(faces)}")

  @commands.command()
  async def mock(self, ctx, *, sentence):
    '''Return a mocking sentence'''
    new_sentence = ''.join(c.lower() if random.randrange(2) else c.upper() for c in sentence)
    await ctx.send(new_sentence)

  @commands.command()
  async def say(self, ctx, *, args):
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

  @commands.command()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def aww(self, ctx):
      '''Get a random image from r/aww'''
      loading_message = await ctx.send(f"{heart} Now loading... {heart}")
      try:
          reddit = config.reddit
          subreddit = reddit.subreddit('aww')
          hot_aww = subreddit.hot(limit=100)
          img_subs = []
          for submission in hot_aww:
              submission_end = submission.url[-3:]
              if submission_end in ["jpg", "png"]:
                  img_subs.append(submission)
          img_sub = random.choice(img_subs)
          img_sub.title = (
              img_sub.title[:253] + "...") if len(img_sub.title) > 256 else img_sub.title
          url = f"https://www.reddit.com{img_sub.permalink}"
          aww_embed = discord.Embed(
              title=img_sub.title, url=url, color=discord.Color.purple())
          print(img_sub.permalink)
          aww_embed.set_image(url=img_sub.url)
          await ctx.send(content="", embed=aww_embed)
      finally:
          await loading_message.delete()

def setup(bot):
  bot.add_cog(Fun(bot))
