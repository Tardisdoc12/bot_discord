################################################################################
# filename: tags_user.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import app_commands

from bot import bot, id_channel_command
from functions.core import check_channel_id
from functions.users import register_member
from functions.tags_users import add_tags, get_tags_for_user, delete_tag
from bdd.tags_users_bdd import tags

################################################################################
#TAGS COMMANDS:

@bot.tree.command(name="add_tags", description="ajoute un tag au profil")
async def add_tag(interaction: discord.Interaction, tag : str):
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    if tag in tags:
        await add_tags(interaction, tag)
    else:
        await interaction.response.send_message("Ce tag n'existe pas.")

################################################################################

@bot.tree.command(name="get_tags", description="Donne tous les tags")
async def get_tags(interaction: discord.Interaction):
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    await interaction.response.send_message(", ".join(tags))

################################################################################

@bot.tree.command(name="get_tags_user", description="Donne tous les tags d'un utilisateur")
async def get_tags_user(interaction: discord.Interaction, user_name : str = None):
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    await get_tags_for_user(interaction, user_name)

################################################################################

@bot.tree.command(name="delete_tag_user", description="Supprime un tag de l'utilisateur")
async def delete_tag_user(interaction: discord.Interaction, tag : str):
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    await delete_tag(interaction, tag)

################################################################################

@delete_tag_user.autocomplete("tag")
@add_tag.autocomplete("tag")
async def name_tags(interaction: discord.Interaction, current_input : str):
    tags_name = []

    # Liste de tous les tags possibles (ex: récupérés depuis ta base de données ou en mémoire)
    all_tags = tags  # Assure-toi que `tags` est une liste accessible ici

    # Filtrage intelligent : on garde les tags contenant la saisie (insensible à la casse)
    filtered = sorted(
        [tag for tag in all_tags if current_input.lower() in tag.lower()],
        key=lambda x: x.lower().find(current_input.lower())
    )

    # Limite à 25 suggestions max
    filtered = filtered[:25]

    # Création des objets Choice
    tags_name = [app_commands.Choice(name=tag, value=tag) for tag in filtered]

    return tags_name

################################################################################

@get_tags_user.autocomplete("user_name")
async def nom_autocomplete(interaction: discord.Interaction, current: str):

    all_names = interaction.guild.fetch_members(limit=None)

    filtered = sorted(
        [member.name async for member in all_names if current.lower() in member.display_name.lower()],
        key=lambda x: x.lower().find(current.lower())
    )[:25]

    users_name = [app_commands.Choice(name=member_name, value=member_name) for member_name in filtered]
    
    return users_name

################################################################################
# End of File
################################################################################