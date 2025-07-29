################################################################################
# filename: city.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 29/07,2025
################################################################################

import discord

from bot import bot, id_channel_command
import functions.city_user as city_user
from functions.core import check_channel_id
from functions.users import miss_profil

################################################################################

@bot.tree.command(name="add_city", description="Ajoute une ville au profil")
async def add_city(interaction: discord.Interaction, city: str) -> None:
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    isGoodChannel = await check_channel_id(interaction, id_channel_command)
    if not isGoodChannel:
        await interaction.response.send_message("Vous devez utiliser cette commande dans les salons autorisés",ephemeral=True)
        return
    await interaction.response.defer()
    
    is_city_already_in_user = city_user.add_city_to_user(interaction.user.id, city)
    if not is_city_already_in_user:
        await interaction.edit_original_response(content=f"Ville {city} ajoutée.",ephemeral=True)
        return
    else:
        await interaction.edit_original_response(content=f"une ville a déjà été ajoutée veuillez utiliser la commande /update_city.",ephemeral=True)
        return

################################################################################

@bot.tree.command(name="update_city", description="Met à jour une ville")
async def update_city(interaction: discord.Interaction, new_city: str, old_city: str) -> None:
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    isGoodChannel = await check_channel_id(interaction, id_channel_command)
    if not isGoodChannel:
        await interaction.response.send_message("Vous devez utiliser cette commande dans les salons autorisés",ephemeral=True)
        return
    
    await interaction.response.defer()
    
    is_city_already_in_user = city_user.update_city_from_user(interaction.user.id, new_city, old_city)
    if not is_city_already_in_user:
        await interaction.edit_original_response(content=f"Aucune ville trouvée pour votre profil. Veuillez utiliser la commande /add_city.",ephemeral=True)
        return
    else:
        await interaction.edit_original_response(content=f"Ville {new_city} mis à jour.",ephemeral=True)
        return

################################################################################

@bot.tree.command(name="delete_city", description="Supprime une ville")
async def delete_city(interaction: discord.Interaction, city: str) -> None:
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    isGoodChannel = await check_channel_id(interaction, id_channel_command)
    if not isGoodChannel:
        await interaction.response.send_message("Vous devez utiliser cette commande dans les salons autorisés",ephemeral=True)
        return
    
    await interaction.response.defer()
    
    is_city_already_in_user = city_user.delete_city_from_user(interaction.user.id, city)
    if not is_city_already_in_user:
        await interaction.edit_original_response(content=f"Aucune ville trouvée pour votre profil. Veuillez utiliser la commande /add_city.",ephemeral=True)
        return
    else:
        await interaction.edit_original_response(content=f"Ville {city} supprimée.",ephemeral=True)
        return

################################################################################
# End of File
################################################################################