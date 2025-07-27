################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import app_commands

from bot import bot, id_channel_command
from functions.core import check_channel_id
from functions.users import miss_profil
from functions.urls import create_url, update_url_from_user, delete_url_from_user, get_urls_from_user

################################################################################

@bot.tree.command(name="add_urls", description="Ajoute une url au profil")
async def add_urls(interaction: discord.Interaction, url : str):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
    if not check_channel_id(interaction, id_channel_command):
        return
    create_url(interaction.user.id, url)
    await interaction.response.send_message(f"URL {url} ajoutée.")

################################################################################

@bot.tree.command(name="update_urls", description="Met à jour une url")
async def update_urls(interaction: discord.Interaction, new_url : str, old_url : str):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
    if not check_channel_id(interaction, id_channel_command):
        return
    update_url_from_user(interaction, old_url, new_url)
    await interaction.response.send_message(f"URL {new_url} mis à jour.")

################################################################################

@bot.tree.command(name="delete_urls", description="Supprime une url")
async def delete_urls(interaction: discord.Interaction, url : str):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
    if not check_channel_id(interaction, id_channel_command):
        return
    delete_url_from_user(interaction.user.id, url)
    await interaction.response.send_message(f"URL {url} supprimée.")

################################################################################

@bot.tree.command(name="get_urls_user", description="Donne toutes les urls d'un utilisateur")
async def get_urls_user(interaction: discord.Interaction, user_name : str = None):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
    if not check_channel_id(interaction, id_channel_command):
        return
    urls = get_urls_from_user(interaction, user_name if user_name else interaction.user.id)
    if urls == []:
        await interaction.response.send_message("Aucune URL n'a été ajoutée.")
    else:
        urls = ["\t" + url for url in urls]
        urls = ",\n".join(urls)
        await interaction.response.send_message(urls)

################################################################################

@get_urls_user.autocomplete("user_name")
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