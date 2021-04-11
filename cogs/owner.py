import config
import os

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

guild_ids = config.GUILDS


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="reload",
                       description="Commande administrateur, permet de recharger les modules du bot.",
                       options=[
                           create_option(
                               name="module",
                               description="Optionnel : module à recharger.",
                               option_type=3,
                               required=False
                           )
                       ],
                       guild_ids=guild_ids)
    async def _reload(self, ctx: SlashContext, module: str = None):
        await ctx.defer(hidden=True)
        if module is not None:
            self.bot.unload_extension(f'cogs.{module}')
            self.bot.load_extension(f'cogs.{module}')
            print(f'Rechargement du module {module}')
            await ctx.send(f'Le module {module} a été rechargé !', hidden=True)
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Rechargement du module {filename[:-3]}')
            await ctx.send(f'Tous les modules ont étés rechargés !', hidden=True)


def setup(bot):
    bot.add_cog(Owner(bot))
