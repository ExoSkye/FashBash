import discord
from discord.ext import commands
import pymongo

from log import logger
import config


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(DBCog(bot))


class DBCog(commands.Cog):
    mongo_r: pymongo.MongoClient
    mongo_rw: pymongo.MongoClient

    def __init__(self, bot):
        self.bot = bot
        self.mongo_r = pymongo.MongoClient(
            f"mongodb+srv://{config.get_config('mongo_db_r_user')}:{config.get_config('mongo_db_r_passwd')}@{config.get_config('mongo_db_url')}/{config.get_config('mongo_db_name')}?retryWrites=true&w=majority"
        )
        self.mongo_rw = pymongo.MongoClient(
            f"mongodb+srv://{config.get_config('mongo_db_rw_user')}:{config.get_config('mongo_db_rw_passwd')}@{config.get_config('mongo_db_url')}/{config.get_config('mongo_db_name')}?retryWrites=true&w=majority"
        )
        logger.info(f"Successfully connected to MongoDB {config.get_config('mongo_db_name')}")
