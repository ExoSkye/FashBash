import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

import pyodbc
import datetime
import traceback
import aiohttp

load_dotenv()

bot = commands.Bot(command_prefix=".")
db: pyodbc.Connection = pyodbc.connect(os.environ["SQL_RW_STRING"])


async def checkBan(id) -> list:
    cursor: pyodbc.Cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM FashBash.dbo.BANS WHERE ID=?
    """, [id])
    output = cursor.fetchall()
    cursor.close()
    return output


async def addBan(id, reason, server) -> None:
    cursor: pyodbc.Cursor = db.cursor()
    cursor.execute("""
        INSERT INTO FashBash.dbo.BANS (ID,REASON,SERVER,EXPIRE)
        VALUES (?,?,?,?)
    """, [id, reason, server, datetime.date.today() + datetime.timedelta(days=365)])
    cursor.commit()
    cursor.close()


async def unBan(id) -> None:
    cursor: pyodbc.Cursor = db.cursor()
    cursor.execute("""
            UPDATE FashBash.dbo.BANS
            SET EXPIRE = ?
            WHERE ID=?
        """, [datetime.date(0, 0, 0), id])
    cursor.close()


@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Command failed. You might've mistyped the command, check `.help`")
    print(error)


@bot.command(name="report")
async def report(ctx, arg1, *oargs):
    user = await commands.UserConverter().convert(ctx, arg1)
    await addBan(user.id, " ".join(oargs), ctx.guild.id)


@bot.command(name="check")
async def check(ctx, args):
    args = args.split(" ")
    user = await commands.UserConverter().convert(ctx, args[0])
    output = await checkBan(user.id)
    if len(output) > 0:
        output = output[0]
        banned_on = await commands.GuildConverter().convert(ctx, str(output[2]))
        await ctx.send("User was previously banned\nServer: " + banned_on.name + "\nExpires: " + str(output[3].day) + "/" + str(output[3].month) + "/" + str(output[3].year) + "\nReason: " + output[1])
    else:
        await ctx.send("User hasn't been banned previously")


bot.run(os.environ["TOKEN"])
