################################################################################
# filename: profile.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord

from bot import bot, id_channel_command
from functions.core import check_channel_id
from functions.users import register_member
from functions.profil_user import create_profile

################################################################################

@bot.tree.command(name="get_profile", description="Donne le profil de l'utilisateur")
async def get_profile(interaction: discord.Interaction, user_name : str = None) -> str:
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    profile_embed = await create_profile(user_name, interaction)
    if profile_embed is None:
        await interaction.response.send_message("Utilisateur introuvable.")
    else:
        await interaction.response.send_message(embed=profile_embed)

################################################################################
# End of File
################################################################################