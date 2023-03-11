import discord
import config as cfg
import os
from discord.ext import commands

intents = discord.Intents.all()

# add help_command=None to disable the default help command
client = commands.Bot(command_prefix=cfg.PREFIX,
                      intents=intents)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            # await client.load_extension(f"cogs.{filename[:-3]}")
            # print(f"Loaded {filename[:-3]}.")
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
            except commands.ExtensionError as e:
                print(f"{filename[:-3]} could not be loaded.")
                print(e)


@client.event
async def on_ready():
    await load_extensions()
    print('Bot is ready.')


@client.listen()
async def on_message(message):
    ctx = await client.get_context(message)
    if not ctx.author.bot and "gay" in ctx.message.content.lower() and not ctx.command:
        await ctx.send(f'{ctx.author} said gay')

client.run(cfg.DISCORD_TOKEN)
