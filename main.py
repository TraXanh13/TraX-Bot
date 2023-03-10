import discord
import praw
import config as cfg
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix=cfg.PREFIX,
                      intents=intents, help_command=None)

reddit = praw.Reddit(client_id=cfg.REDDIT_CLIENT_ID,
                     client_secret=cfg.REDDIT_CLIENT_SECRET,
                     username=cfg.REDDIT_USERNAME,
                     password=cfg.REDDIT_PASSWORD,
                     user_agent=cfg.REDDIT_USER_AGENT)


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def subredd(ctx, sub="meme"):
    subreddit = reddit.subreddit(sub)

    if (subreddit.over18 and not ctx.message.channel.is_nsfw()):
        sfwRedd = reddit.subreddit("catswithjobs").random()
        await ctx.send(f'{ctx.author} this subreddit is NSFW, here is a random post instead: {sfwRedd.url}')
        return

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
@commands.is_nsfw()
async def porn(ctx):
    subreddit = reddit.subreddit("porn")

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
@commands.is_nsfw()
async def gay(ctx):
    subreddit = reddit.subreddit('GayPorn')

    random = subreddit.random()

    await ctx.send(random.url)


@client.command()
async def help(ctx):
    if (ctx.message.channel.is_nsfw()):
        await ctx.send(embed=makeEmbed(title="Commands:", description="```\n.ping\n.subredd\n.porn\n.gay\n.help```"))
    else:
        await ctx.send(embed=makeEmbed(title="Commands:", description="```\n.ping\n.subredd\n.help```"))


@client.listen()
async def on_message(message):
    ctx = await client.get_context(message)
    if not ctx.author.bot and "gay" in ctx.message.content.lower() and not ctx.command:
        await ctx.send(f'{ctx.author} said gay')


@client.command()
async def embed(ctx):
    message = ctx.message.content.split("\"")[1::2]
    title = message[0]
    description = message[1]

    if len(message) > 2 and len(message) % 2 == 0:
        fields = {}
        for i in range(2, len(message), 2):
            fields[message[i]] = message[i+1]

        await ctx.send(embed=makeEmbed(title=title, description=description, **fields))
    else:
        await ctx.send(embed=makeEmbed(title=title, description=description))


def makeEmbed(title="", url=None, description=None, color=0x00ff00, **fields):
    if (url == None):
        embed = discord.Embed(title=title,
                              description=description, color=color)
    else:
        embed = discord.Embed(title=title, url=url,
                              description=description, color=color)

    for name, value in fields.items():
        embed.add_field(name=name, value=value, inline=False)
    return embed


client.run(cfg.DISCORD_TOKEN)
