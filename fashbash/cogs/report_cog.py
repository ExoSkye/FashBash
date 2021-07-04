import discord
from discord.ext import commands

from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext

import datetime
import bot
import db_cog
from log import logger
import config


def setup(bot):
    bot.add_cog(ReportCog(bot))


class ReportCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.db: db_cog.DBCog = bot.get_cog("DBCog")
        if self.db is None:
            logger.error("Could not get database cog, exiting")
            raise ModuleNotFoundError

    @cog_ext.cog_slash(
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
        ]
    )
    async def report(self, ctx, user, reason):
        if ctx.author.guild_permissions.ban_members:
            collection = self.db.mongo_rw["fashbash"]["bans"]
            collection.insert_one({"id": user.id,
                                   "reason": reason,
                                   "server": ctx.guild.id,
                                   "expire_day": datetime.datetime.now().day,
                                   "expire_month": datetime.datetime.now().month,
                                   "expire_year": datetime.datetime.now().year + 1
                                   })
            await ctx.send("Reported " + user.name)
        else:
            await ctx.send("You aren't allowed to do that")
