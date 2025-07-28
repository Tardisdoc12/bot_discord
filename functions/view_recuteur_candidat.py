################################################################################
# filename: view_recuteur_candidat.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 27/07,2025
################################################################################

import discord

from bdd.tags import tag_kind_people, channels_for_everyone, tag_by_channels
from roles.role_base import get_or_create_role

################################################################################

class ViewCreationRecruteurCandidat(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    
    @discord.ui.button(label="Recruteur", style=discord.ButtonStyle.primary,custom_id="view:recruteur")
    async def recruteur(self, interaction: discord.Interaction, button: discord.ui.Button):
        recruteur_role_name = tag_kind_people[0]
        channels_available = channels_for_everyone + tag_by_channels[recruteur_role_name]
        recruteur_role = await get_or_create_role(recruteur_role_name, interaction.guild, discord.Colour.green(),salons=channels_available)
        if recruteur_role in interaction.user.roles:
            await interaction.user.remove_roles(recruteur_role)
            await interaction.response.send_message("Vous avez retiré le role recruteur", ephemeral=True)
        else:
            await interaction.user.add_roles(recruteur_role)
            await interaction.response.send_message("Vous avez ajouté le role recruteur", ephemeral=True)


    @discord.ui.button(label="Candidat", style=discord.ButtonStyle.primary,custom_id="view:candidat")
    async def candidat(self, interaction: discord.Interaction, button: discord.ui.Button):
        candidat_role_name = tag_kind_people[1]
        candidat_role = await get_or_create_role(candidat_role_name, interaction.guild, discord.Colour.green(),salons=channels_for_everyone)
        if candidat_role in interaction.user.roles:
            await interaction.user.remove_roles(candidat_role)
            await interaction.response.send_message("Vous avez retiré le role candidat", ephemeral=True)
        else:
            await interaction.user.add_roles(candidat_role)
            await interaction.response.send_message("Vous avez ajouté le role candidat", ephemeral=True)

################################################################################
# End of File
################################################################################