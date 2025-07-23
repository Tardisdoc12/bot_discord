################################################################################
# filename: routes.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import os

import dotenv
import discord
from discord.ext import commands
from discord import app_commands

from functions.core import (
    check_channel_id,
)
from functions.user_resume import (
    download_pdf,
    give_resume,
)
from bdd.init_bdd import (
    init_db,
)

################################################################################
#ENVIRONMENT VARIABLES:

dotenv.load_dotenv()
init_db()

################################################################################
#CONSTANTS:

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire les messages
intents.members = True
id_channel_command = int(os.getenv("ID_CHANNEL_COMMAND"))

bot = commands.Bot(command_prefix="!", intents=intents)

################################################################################
#EVENTS:

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=discord.Object(id=int(os.getenv("GUILD_ID"))))
    await bot.tree.sync(guild=discord.Object(id=int(os.getenv("GUILD_ID"))))
    print(f"Bot connecté en tant que {bot.user}")

################################################################################
#COMMANDS:

@bot.tree.command(name="resume_send", description="Sauvegarde le CV de l'utilisateur")
async def resume_send(interaction: discord.Interaction, fichier: discord.Attachment):
    if not check_channel_id(interaction, id_channel_command):
        return
    await download_pdf(interaction, fichier)

@bot.tree.command(name="resume_give", description="Donne le CV de quelqu'un")
async def resume_give(interaction: discord.Interaction, nom : str = None):
    if not check_channel_id(interaction, id_channel_command):
        return
    await give_resume(interaction, nom)

################################################################################

@resume_give.autocomplete("nom")
async def nom_autocomplete(interaction: discord.Interaction, current: str):
    noms = []
    async for member in interaction.guild.fetch_members(limit=None):
        if current.lower() in member.display_name.lower():
            noms.append(app_commands.Choice(name=member.display_name, value=str(member.name)))

    return noms

################################################################################
#RUNNING THE BOT:

bot.run(os.getenv("TOKEN_BOT"))

################################################################################
# End of File
################################################################################