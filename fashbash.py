import logging
import os
import tabulate
import git
from git import *
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import pymongo
import datetime
import subprocess

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = commands.Bot(command_prefix=".", description="")
slash = SlashCommand(bot, sync_commands=True)
mongo_client_rw = pymongo.MongoClient(
    "mongodb+srv://" + os.environ["MONGO_RW_USER"] + ":" + os.environ["MONGO_RW_PWD"] + "@" + os.environ[
        "MONGO_DOMAIN"] + "/" + os.environ["MONGO_DB"] + "?retryWrites=true&w=majority")
mongo_client_r = pymongo.MongoClient(
    "mongodb+srv://" + os.environ["MONGO_R_USER"] + ":" + os.environ["MONGO_R_PWD"] + "@" + os.environ[
        "MONGO_DOMAIN"] + "/" + os.environ["MONGO_DB"] + "?retryWrites=true&w=majority")


async def checkBan(id) -> (list, int):
    collection = mongo_client_r["fashbash"]["bans"]
    query = {"id": id}
    count = collection.count_documents(query)
    if count > 0:
        doc = collection.find(query)
        return doc, count
    else:
        return [], count


async def addBan(id, reason, server) -> None:
    collection = mongo_client_rw["fashbash"]["bans"]
    collection.insert_one({"id": id,
                       "reason": reason,
                       "server": server,
                       "expire_day": datetime.datetime.now().day,
                       "expire_month": datetime.datetime.now().month,
                       "expire_year": datetime.datetime.now().year + 1
                       })


async def unBan(id) -> None:
    collection = mongo_client_rw["fashbash"]["bans"]
    collection.update({"id": id}, {"$set": {"expire_year": 0}})


@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Command failed. You might've mistyped the command, check `.help`")
    print(error)


@slash.slash(
    name="report",
    description="Report a user to the DB",
    options=[
        create_option(name="user",
                      description="User to report",
                      option_type=6,
                      required=True),
        create_option(name="reason",
                      description="Reason for report",
                      option_type=3,
                      required=True)
    ])
async def report(ctx, user, reason):
    if discord.abc.GuildChannel.permissions_for(ctx.channel, ctx.author).administrator:
        await addBan(user.id, reason, ctx.guild.id)
        await ctx.send("Reported " + user.name)
    else:
        await ctx.send("You aren't allowed to do that")


@slash.slash(
    name="check",
    description="Checks if a user has been reported to the DB",
    options=[
        create_option(name="user",
                      description="User to report",
                      option_type=6,
                      required=True)
    ])
async def check(ctx, user):
    output, bans = await checkBan(user.id)
    if bans > 0:
        output_str = "**User was previously banned**\n"
        i = 0
        for ban in output:
            banned_on = await commands.GuildConverter().convert(ctx, str(ban["server"]))
            output_str += ("**Ban " + str(i + 1) + ":**\nServer: " + banned_on.name + "\nExpires: " + str(
                ban["expire_day"]) + "/" + str(ban["expire_month"]) + "/" + str(ban["expire_year"]) + "\nReason: " + ban["reason"] + "\n")
            i += 1
        await ctx.send(output_str)
    else:
        await ctx.send("User hasn't been banned previously")


@slash.slash(
    name="fashbash",
    description="Gets some information about FashBash"
)
async def fashbash(ctx: SlashContext):
    repo = Repo(os.getcwd())
    o = repo.remotes.origin
    o.pull()
    commits = list(repo.iter_commits())

    count = {}

    for commit in commits:
        try:
            count[commit.author.name] += 1
        except KeyError:
            count[commit.author.name] = 1

    sorted_count = dict(sorted(count.items(), key=lambda item: item[1]))

    sorted_count = [{x[0], str(x[1])} for x in sorted_count.items()]

    output = tabulate.tabulate(sorted_count, ["Committer", "Commits"], tablefmt="grid")
    await ctx.send(
        """**FashBash**
FashBash is a small bot which syncs bans between servers and is designed for the leftist community to keep fascist ancaps and the like from raiding their server
The GitHub repo is: https://github.com/ProtoByter/FashBash
**Contributors**
```""" + output + "```")


@bot.event
async def on_ready():
    print("Ready!")


bot.run(os.environ["TOKEN"])
