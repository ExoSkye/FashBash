import discord
from discord.ext import commands

from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext

import bot
import db_cog
from log import logger
import config

def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(CheckCog(bot))

class CheckCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.db: db_cog.DBCog = bot.get_cog("DBCog")
        if self.db is None:
            logger.error("Could not get database cog, exiting")
            raise ModuleNotFoundError

    @cog_ext.cog_slash(
        name="check",
        description="Checks if a user has been reported to the DB",
        options=[
            create_option(name="user",
                          description="User to report",
                          option_type=6,
                          required=True)
        ]
    )

    async def check(self, ctx, user):
        collection = self.db.mongo_r["fashbash"]["bans"]
        query = {"id": user.id}
        count = collection.count_documents(query)
        if count > 0:
            output = collection.find(query)
            output_str = "**User was previously banned**\n"
            i = 0
            for ban in output:
                banned_on: discord.Guild = await commands.GuildConverter().convert(ctx, str(ban["server"]))
                expire_date = f"{ban['expire_day']}/{ban['expire_month']}/{ban['expire_year']}"
                output_str += f"**Ban {i + 1}:**\nServer: {banned_on.name}\nExpires: {expire_date}\nReason: {ban['reason']}\n"
                i += 1
            await ctx.send(output_str)
        else:
            await ctx.send("User hasn't been banned previously")

