################################################################################
# filename: resume.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import app_commands

from bot import bot, id_channel_command
from functions.user_resume import download_pdf, give_resume
from functions.core import check_channel_id
from functions.users import miss_profil

################################################################################

@bot.tree.command(name="send_resume", description="Sauvegarde le CV de l'utilisateur")
async def resume_send(interaction: discord.Interaction, fichier: discord.Attachment):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    isGoodChannel = await check_channel_id(interaction, id_channel_command)
    if not isGoodChannel:
        return
    await download_pdf(interaction, fichier)

################################################################################

@bot.tree.command(name="give_resume", description="Donne le CV de quelqu'un")
async def resume_give(interaction: discord.Interaction, nom : str = None):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    isGoodChannel = await check_channel_id(interaction, id_channel_command)
    if not isGoodChannel:
        return
    await give_resume(interaction, nom)

################################################################################

@resume_give.autocomplete("nom")
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