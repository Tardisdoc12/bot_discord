################################################################################
# filename: profile.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import app_commands

from bot import bot, id_channel_command
from functions.core import check_channel_id,UrlModal
from functions.users import register_member
from functions.profil_user import create_profile, get_profil_photo_user_name, get_profil
from functions.temp_stockage import temp_data
from functions.view_creation_base import ViewCreationBase

################################################################################

class UserProfileView(ViewCreationBase):
    def __init__(self, user_id):
        super().__init__(user_id=user_id)
        self.user_id = user_id

    @discord.ui.button(label="Ajouter un url", style=discord.ButtonStyle.primary)
    async def add_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return
        await interaction.response.send_modal(UrlModal(user_id=self.user_id))

    @discord.ui.button(label="Créer le profile", style=discord.ButtonStyle.success)
    async def create_profile(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return

        data = temp_data.pop(self.user_id, None)
        if not data:
            await interaction.response.send_message("Aucune donnée trouvée.", ephemeral=True)
            return
        

        photo = await get_profil_photo_user_name(interaction.user.name, interaction)
        profil_embed = get_profil(
            interaction.user.name,
            data["tags"],
            data["urls"],
            photo
        )

        await interaction.response.send_message("Profil créer :",embed=profil_embed)

################################################################################

@bot.tree.command(name="get_profile", description="Donne le profil de l'utilisateur")
async def get_profile(interaction: discord.Interaction, user_name : str = None) -> str:
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    user_name = user_name if user_name else interaction.user.name
    profile_embed = await create_profile(user_name, interaction)
    if profile_embed is None:
        await interaction.response.send_message("Utilisateur introuvable.")
    else:
        await interaction.response.send_message(embed=profile_embed)

################################################################################

@get_profile.autocomplete("user_name")
async def nom_autocomplete(interaction: discord.Interaction, current: str):

    all_names = interaction.guild.fetch_members(limit=None)

    filtered = sorted(
        [member.name async for member in all_names if current.lower() in member.display_name.lower()],
        key=lambda x: x.lower().find(current.lower())
    )

    users_name = [app_commands.Choice(name=member_name, value=member_name) for member_name in filtered]
    
    return users_name

################################################################################

@bot.tree.command(name="create_profile", description="Créer le profile de l'utilisateur")
async def create_profile(interaction: discord.Interaction):
    register_member(interaction)
    if not check_channel_id(interaction, id_channel_command):
        return
    await interaction.response.send_message("Créer le profile", view=UserProfileView(interaction.user.id))

################################################################################
# End of File
################################################################################