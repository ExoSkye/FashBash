import discord
from discord.ext import commands

import bot
from discord_slash import cog_ext


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(InfoCog(bot))


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed = discord.Embed(title="FashBash",
                                   description="FashBash is a small bot which syncs bans between servers and is "
                                               "designed for the leftist community to keep fascist ancaps and the "
                                               "like from raiding their server")
        self.embed.add_field(name="GitHub Repo", value="https://github.com/ProtoByter/FashBash", inline=False)

    @cog_ext.cog_slash(
        name="fashbash",
        description="Returns some information about FashBash"
    )
    async def fashbash(self, ctx):
        await ctx.send(embed=self.embed)
