import os

import discord
from discord.ext import commands

import config
from log import configure_logger, logger
import utils

config.create_config()
configure_logger() # see notes in log.py

token = config.get_config("token")
prefix = config.get_config("prefix")

bot = commands.Bot(
    command_prefix=prefix,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help"
    )
)

# Funny dynamic typing stuff so that we can access the bot object outside here
utils.bot = bot

# Loading the cogs
if __name__ == "__main__":
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            bot.load_extension("cogs." + file[:-3])

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}")