################################################################################
# filename: view_creation_base.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from functions.core import TagSelectView
from bdd.tags import tags_metier, tags_framework, tags_language

################################################################################

class ViewCreationBase(discord.ui.View):
    def __init__(self, user_id, timeout=300):
        super().__init__(timeout = timeout)
        self.user_id = user_id

    @discord.ui.button(label="Ajouter un type", style=discord.ButtonStyle.primary)
    async def add_tag(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return
        await interaction.response.send_message("Sélectionne un tag :", view=TagSelectView(interaction.user.id, tags_metier,"Selection un type de travail:"), ephemeral=True)

    @discord.ui.button(label="Ajouter un language", style=discord.ButtonStyle.primary)
    async def add_languages(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return
        await interaction.response.send_message("Sélectionne un tag :", view=TagSelectView(interaction.user.id, tags_language,"Selection un language:"), ephemeral=True)

    @discord.ui.button(label="Ajouter un framework", style=discord.ButtonStyle.primary)
    async def add_frameworks(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return
        await interaction.response.send_message("Sélectionne un tag :", view=TagSelectView(interaction.user.id, tags_framework,"Selection un framework:"), ephemeral=True)

################################################################################
# End of File
################################################################################