import os

import discord
from discord.ext import commands

from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

import config
from log import configure_logger, logger
import utils

config.create_config()
configure_logger() # see notes in log.py

token = config.get_config("token")

bot = commands.Bot(
    command_prefix="\t",
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="/fashbash help"
    )
)

slash = SlashCommand(bot)

# Funny dynamic typing stuff so that we can access the bot object outside here
utils.bot = bot

# Loading the cogs
if __name__ == "__main__":

    # Read the priority file

    files = []
    with open("cogs/priority") as priority_file:
        for line in priority_file.read().split("\n"):
            split_line = line.split("|")
            split_line[0] = int(split_line[0])
            files.append(split_line)

    # Add everything else (including priority files)
    non_prio_files = []
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            non_prio_files.append([0,file])

    # Remove priority files from non-priority list
    for prio_file in files:
        for file in non_prio_files:
            if file[1] == prio_file[1]:
                del non_prio_files[non_prio_files.index(file)]

    # Concatenate these two lists
    files += non_prio_files

    # Sort the lists
    files.sort(key=lambda value: value[0],reverse=True)

    # Get the filenames of all the files in order (filenames are file[1])
    filenames = [x[1] for x in files]

    # Actually load these in
    for file in filenames:
        print(f"Trying to load {file}")
        bot.load_extension("cogs." + file[:-3])
        print(f"Loaded {file}")

    bot.run(token)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}")