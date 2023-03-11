import praw
import config as cfg
from discord.ext import commands


class redditCog(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.reddit = praw.Reddit(client_id=cfg.REDDIT_CLIENT_ID,
                                  client_secret=cfg.REDDIT_CLIENT_SECRET,
                                  username=cfg.REDDIT_USERNAME,
                                  password=cfg.REDDIT_PASSWORD,
                                  user_agent=cfg.REDDIT_USER_AGENT)

    @commands.command(name="subreddit", aliases=["subredd", "sub"], help="Gets a random post from a subreddit.")
    async def subredd(self, ctx, sub="meme"):
        subreddit = self.reddit.subreddit(sub)

        if (subreddit.over18 and not ctx.message.channel.is_nsfw()):
            sfwRedd = self.reddit.subreddit("catswithjobs").random()
            await ctx.send(f'{ctx.author} this subreddit is NSFW, here is a random post instead: {sfwRedd.url}')
            return

        random = subreddit.random()

        await ctx.send(random.url)

    @commands.command(name="porn", help="Sends NSFW content from reddit")
    @commands.is_nsfw()
    async def porn(self, ctx):
        subreddit = self.reddit.subreddit("porn")

        random = subreddit.random()

        await ctx.send(random.url)

    @commands.command(name="gay", help="Sends gay NSFW content from reddit")
    @commands.is_nsfw()
    async def gay(self, ctx):
        subreddit = self.reddit.subreddit('GayPorn')

        random = subreddit.random()

        await ctx.send(random.url)


async def setup(client):
    await client.add_cog(redditCog(client))
