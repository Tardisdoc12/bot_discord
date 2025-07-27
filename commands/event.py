################################################################################
# filename: event.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord

from bot import bot, GUILD_ID
from commands.admin import admin
from functions.temp_stockage import persistant_view

################################################################################


# @bot.event
# async def on_ready():
#     global persistant_view
#     persistant_view = ViewCreationRecruteurCandidat()
#     bot.add_view(persistant_view)  # enregistrer la vue persistante
#     bot.tree.add_command(admin)
#     bot.tree.copy_global_to(guild=discord.Object(id=int(GUILD_ID)))
#     await bot.wait_until_ready()
#     await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
#     print(f"Bot connecté en tant que {bot.user}")


################################################################################
# End of File
################################################################################