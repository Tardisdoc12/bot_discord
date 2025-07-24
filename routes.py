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
from functions.tags import (
    get_tags_for_user,
    get_users_name_from_tag,
    add_tags,
    delete_tag,
)
from functions.profil_user import (
    create_profile,
)
from bdd.init_bdd import (
    init_db,
)
from bdd.tags_bdd import (
    tags,
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
#RESUME COMMANDS:

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
#TAGS COMMANDS:

@bot.tree.command(name="add_tags", description="ajoute un tag au profil")
async def add_tag(interaction: discord.Interaction, tag : str):
    if not check_channel_id(interaction, id_channel_command):
        return
    if tag in tags:
        await add_tags(interaction, tag)
    else:
        await interaction.response.send_message("Ce tag n'existe pas.")

@bot.tree.command(name="get_tags", description="Donne tous les tags")
async def get_tags(interaction: discord.Interaction):
    if not check_channel_id(interaction, id_channel_command):
        return
    await interaction.response.send_message(", ".join(tags))

@bot.tree.command(name="get_tags_user", description="Donne tous les tags d'un utilisateur")
async def get_tags_user(interaction: discord.Interaction, user_name : str = None):
    if not check_channel_id(interaction, id_channel_command):
        return
    await get_tags_for_user(interaction, user_name)

@bot.tree.command(name="get_users_from_tag", description="Donne tous les utilisateurs ayant un tag")
async def get_users_from_tag(interaction: discord.Interaction, tag : str):
    if not check_channel_id(interaction, id_channel_command):
        return
    await get_users_name_from_tag(tag, interaction)

@bot.tree.command(name="delete_tag_user", description="Supprime un tag de l'utilisateur")
async def delete_tag_user(interaction: discord.Interaction, tag : str):
    if not check_channel_id(interaction, id_channel_command):
        return
    await delete_tag(interaction, tag)

################################################################################
# COMMANDS PROFILE:

@bot.tree.command(name="get_profile", description="Donne le profil de l'utilisateur")
async def get_profile(interaction: discord.Interaction, user_name : str = None) -> str:
    if not check_channel_id(interaction, id_channel_command):
        return
    profile_embed = await create_profile(user_name, interaction)
    if profile_embed is None:
        await interaction.response.send_message("Utilisateur introuvable.")
    else:
        await interaction.response.send_message(embed=profile_embed)

################################################################################
# AUTOCOMPLETE COMMANDS:

@get_profile.autocomplete("user_name")
@get_tags_user.autocomplete("user_name")
@resume_give.autocomplete("nom")
async def nom_autocomplete(interaction: discord.Interaction, current: str):
    noms = []
    async for member in interaction.guild.fetch_members(limit=None):
        if current.lower() in member.display_name.lower():
            noms.append(app_commands.Choice(name=member.display_name, value=str(member.name)))
    return noms

@delete_tag_user.autocomplete("tag")
@get_users_from_tag.autocomplete("tag")
@add_tag.autocomplete("tag")
async def name_tags(interaction: discord.Interaction, tag : str):
    tags_name = []
    for tag in tags[:25]:
        tags_name.append(app_commands.Choice(name=tag, value=tag))
    return tags_name

################################################################################
#RUNNING THE BOT:

bot.run(os.getenv("TOKEN_BOT"))

################################################################################
# End of File
################################################################################