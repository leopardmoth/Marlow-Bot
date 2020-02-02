# import necessary modules
import random
import discord
import config
from discord.ext import commands

# creates a bot instance with "$" as the command prefix
bot = commands.Bot("$")
client = discord.Client()

TOKEN = config.TOKEN

header = {"User-Agent": "Magic Browser"}
heart = '<a:loading_heart:542883297600995349>'
staff = {'Admin': 553314578528993311,
         'Mod': 553356112636936203}
muted = 553358001550131208
testing = 553314472341536776

# This is how you define a discord.py event
@bot.event
async def on_ready():  # the event `on_ready` is triggered when the bot is ready to function
    print(f"{format(bot.user.name)} is online.")
    bot.load_extension("cogs.Utility")
    bot.load_extension("cogs.Fun")
    await bot.change_presence(activity=discord.Activity(name="Despacito", type=discord.ActivityType.listening))
    channel = bot.get_channel(testing)
    await channel.send("Bot is online.")


@bot.event
async def on_command_error(ctx, e):
    if hasattr(ctx.command, 'on_error'):
        print(type(e), e)
        return

    e = getattr(e, 'original', e)

    ignored = (commands.CommandNotFound, commands.UserInputError)

    if isinstance(e, ignored):
        return

    elif isinstance(e, commands.CommandOnCooldown):
        return await ctx.send(f'Stop spamming! Try again in {round(e.retry_after)+1} second(s).')
    elif isinstance(e, commands.CheckFailure):
        return await ctx.send(f"I only respond to my mom.")
    elif isinstance(e, commands.MissingPermissions):
        return await ctx.send(f"You are missing these ({list.missing_perms}) to run this command.")
    elif isinstance(e, commands.BotMissingPermissions):
        return await ctx.send(f"I need these permissions ({list.missing_perms}) to run this command.")
    elif isinstance(e, commands.DisabledCommand):
        return await ctx.send(f"Command is disabled.")
    elif isinstance(e, discord.HTTPException):
        return await ctx.send(f"**Error:** {e}")
    elif isinstance(e, commands.CommandError):
        return await ctx.send(f"**Error:** {e}")
    else:
        print(type(e), e)
        return
    # await asyncio.sleep(5)
    # await message.delete()
    # try: await ctx.message.delete()
    # except discord.HTTPException: pass


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if random.randrange(4) == 0:
        if 'uwu' in message.content:
            await message.channel.send('uwu')
        if 'OwO' in message.content:
            await message.channel.send('whats this?')
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(555216652589858816)
    message = 'Hello {}! Please enjoy your stay.'.format(member.mention)
    await channel.send(message)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(555216652589858816)
    message = 'Goodbye {}! We will miss you!'.format(member.mention)
    await channel.send(message)

initial_extensions = ["cogs.Utility,cogs.Fun"]
cogs_dir = "cogs"

if __name__ == '__cogs__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))


@bot.command()
@commands.is_owner()
async def unload(ctx, extension_name: str):
    try:
        extension_dir = f"{cogs_dir}.{extension_name}"
        bot.unload_extension(extension_dir)
        await ctx.send("{} unloaded.".format(extension_name))
    except Exception as error:
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension_name, error))
        print('{} cannot be unloaded. [{}]'.format(extension_name, error))


@bot.command()
@commands.is_owner()
async def load(ctx, extension_name: str):
    try:
        extension_dir = f"{cogs_dir}.{extension_name}"
        bot.load_extension(extension_dir)
        await ctx.send("{} loaded.".format(extension_name))
    except Exception as error:
        await ctx.send('{} cannot be loaded. [{}]'.format(extension_name, error))
        print('{} cannot be loaded. [{}]'.format(extension_name, error))


@bot.command()
@commands.is_owner()
async def update(ctx, extension_name: str):
    try:
        extension_dir = f"{cogs_dir}.{extension_name}"
        bot.reload_extension(extension_dir)
        await ctx.send("{} updated.".format(extension_name))
    except Exception as error:
        await ctx.send('{} cannot be updated. [{}]'.format(extension_name, error))
        print('{} cannot be updated. [{}]'.format(extension_name, error))


# starts the bot with the corresponding token
bot.run(TOKEN)
