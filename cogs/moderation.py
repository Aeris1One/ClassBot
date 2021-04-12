import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import config

guild_ids = config.GUILDS


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="mod",
                            name="kick",
                            guild_ids=guild_ids,
                            base_desc="Commandes de modération du serveur.",
                            description="Permet aux modérateurs d'exclure un membre du serveur",
                            options=[
                                create_option(
                                    name="membre",
                                    description="Le membre qui sera exclus aprés l'éxecution de "
                                                "la commande",
                                    option_type=SlashCommandOptionType.USER,
                                    required=True),
                                create_option(
                                    name="reason",
                                    description="Raison de l'exlusion",
                                    option_type=SlashCommandOptionType.STRING,
                                    required=False)
                            ])
    async def _kick(self, ctx: SlashContext, member, reason: str = "Non définie"):
        if ctx.author.guild_permissions.kick_members:
            if member.guild_permissions.administrator:
                await ctx.send(f'Le membre {member} est administrateur, vous ne pouvez pas l\'exclure !', hidden=True)
            else:
                try:
                    embed = discord.Embed(
                        title="Membre exclus",
                        description=f"**{member}** a été exclus du serveur par **{ctx.author}**!",
                        color=config.success
                    )
                    embed.add_field(
                        name="Raison:",
                        value=reason
                    )
                    await ctx.send('Hello', embed=embed, hidden=False)
                    try:
                        await member.send(
                            f"Vous avez été exclus du serveur par **{ctx.author}**!\nRaison: {reason}"
                        )
                    except:
                        pass
                    await member.kick(reason=reason)
                except Exception as e:
                    print(e)
        # await ctx.send('Une erreur est survenue en essayant d\'exclure l\'utilisateur.', hidden=True)
        else:
            await ctx.send(":name_badge: Vous n'avez pas la permission d'exécuter cette commande !", hidden=True)


def setup(bot):
    bot.add_cog(Moderation(bot))
