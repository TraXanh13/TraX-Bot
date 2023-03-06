import discord
import praw
import configTestBot as cfg
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

reddit = praw.Reddit(client_id=cfg.REDDIT_CLIENT_ID,
                     client_secret=cfg.REDDIT_CLIENT_SECRET,
                     username=cfg.REDDIT_USERNAME,
                     password=cfg.REDDIT_PASSWORD,
                     user_agent=cfg.REDDIT_USER_AGENT)


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
@commands.is_nsfw()
async def subredd(ctx, sub="meme"):
    print(sub)
    subreddit = reddit.subreddit(sub)

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
@commands.is_nsfw()
async def porn(ctx, sub="porn"):
    print(sub)
    subreddit = reddit.subreddit(sub)

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
@commands.is_nsfw()
async def gay(ctx):
    subreddit = reddit.subreddit('GayPorn')

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run(cfg.DISCORD_TOKEN)
