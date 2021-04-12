import os

import discord as discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import config

guild_ids = config.GUILDS


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="admin",
                            name="reload",
                            description="Permet de recharger les modules du bot.",
                            base_description="Commandes administrateur de gestion du bot",
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
        if ctx.author_id in config.OWNERS:
            await ctx.defer(hidden=False)
            if module is not None:
                self.bot.unload_extension(f'cogs.{module}')
                self.bot.load_extension(f'cogs.{module}')
                print(f'Rechargement du module {module}')
                embed = discord.Embed(
                    description=f"Le module `{module}` à été rechargé ! :arrows_counterclockwise:",
                    color=config.success
                )
                await ctx.send(embed=embed, hidden=False)
            else:
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.unload_extension(f'cogs.{filename[:-3]}')
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
                        print(f'Rechargement du module {filename[:-3]}')

                embed = discord.Embed(
                    description="Tous les modules ont étés rechargés ! :arrows_counterclockwise:",
                    color=config.success
                )
                await ctx.send(embed=embed, hidden=False)
        else:
            await ctx.send(f'Vous n\'avez pas la permission d\'effectuer cette commande !', hidden=True)

    @cog_ext.cog_subcommand(base="admin",
                            name="shutdown",
                            description="Permet d'éteindre manuellement le bot.",
                            base_description="Commandes administrateur de gestion du bot",
                            guild_ids=guild_ids)
    async def _shutdown(self, ctx):
        if ctx.author_id in config.OWNERS:
            embed = discord.Embed(
                description="Extinction en cours, à bientôt ! :wave:",
                color=config.success
            )
            await ctx.send(embed=embed, hidden=False)
            await self.bot.close()
        else:
            await ctx.send(f'Vous n\'avez pas la permission d\'effectuer cette commande !', hidden=True)


def setup(bot):
    bot.add_cog(Owner(bot))
