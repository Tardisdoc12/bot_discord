################################################################################
# filename: tags.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import discord

from bdd.tags_bdd import (
    get_tags_from_user_name,
    get_all_tags,
    get_tags_from_user_id,
    get_users_from_tag,
    add_tag_to_user,
    delete_tag_user_id,
)

################################################################################

def get_tags_from_user_id_or_name(user_id_or_name : str) -> list:
    if user_id_or_name.isnumeric():
        return get_tags_from_user_id(int(user_id_or_name))
    else:
        return get_tags_from_user_name(user_id_or_name)

################################################################################

async def get_tags_for_user(interaction: discord.Interaction, user_name : str = None) -> list:
   tags = get_tags_from_user_id_or_name( user_name if user_name else str(interaction.user.id))
   if tags:
    message = ",\n".join(list(tags))
    await interaction.response.send_message(message)
   else:
    await interaction.response.send_message("Aucun tag n'a été ajouté.")

################################################################################

async def get_tags(interaction: discord.Interaction) -> list:
    tags = get_all_tags()
    await interaction.response.send_message(tags)

################################################################################

async def get_users_name_from_tag(tag : str, interaction: discord.Interaction) -> list:
    users = get_users_from_tag(tag)
    if not users:
        await interaction.response.send_message("Aucun utilisateur n'a ce tag.")
    else:
        users = ",\n".join(list(users))
        await interaction.response.send_message(users)

################################################################################

async def add_tags(interaction: discord.Interaction, tag : str):
    add_tag_to_user(interaction.user.id, tag)
    await interaction.response.send_message(f"Tag {tag} ajouté à votre profil.")

################################################################################

async def delete_tag(interaction: discord.Interaction, tag : str):
    delete_tag_user_id(interaction.user.id, tag)
    await interaction.response.send_message(f"Tag {tag} supprimé de votre profil.")

################################################################################
# End of File
################################################################################