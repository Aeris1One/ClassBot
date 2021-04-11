import config

from discord.ext import commands
from discord_slash import cog_ext, SlashContext

guild_ids = config.GUILDS


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping", guild_ids=guild_ids)
    async def _ping(self, ctx: SlashContext):
        await ctx.send(content=f"Pong ! :ping_pong: ({int(self.bot.latency * 1000)}ms)", hidden=True)


def setup(bot):
    bot.add_cog(Ping(bot))
