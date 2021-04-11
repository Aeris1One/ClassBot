import asyncio
import discord
import os
import platform
import sys
from discord.ext import commands
from discord_slash import SlashCommand

# RÉCUPERER LA CONFIGURATION
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

# DÉFINIR BOT ET SLASH
bot = commands.Bot(command_prefix=config.BOT_PREFIX)
slash = SlashCommand(bot, override_type=True, sync_commands=True, sync_on_cog_reload=True)

# CHARGER LES COGS
if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            botextension = file[:-3]
            try:
                bot.load_extension(f"cogs.{botextension}")
                print(f"Chargement de l'extension '{botextension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Erreur lors du chargement de l'extension {botextension}\n{exception}")


# ACTION À EFFECTUER AU LANCEMENT CORRECT
@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print(f"Connecté en tant que {bot.user.name}")
    print(f"Version de Discord.py: {discord.__version__}")
    print(f"Version de Python: {platform.python_version()}")
    print(f"Démarré sur: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")


# STATUS DE JEU DU BOT
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(f"Python {platform.python_version()}"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(f"Discord.Py {discord.__version__}"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(f"Essayez '/'"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(f"{platform.system()}"))
        await asyncio.sleep(60)


# LANCER LE BOT
bot.run(config.TOKEN)
