################################################################################
# filename: paginations_embed.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import Interaction, ui

################################################################################

class EmbedPaginator(discord.ui.View):
    def __init__(self, user_id, embed_pages):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.embed_pages = embed_pages
        self.current_page = 0

    async def update_message(self, interaction: Interaction):
        embed = self.embed_pages[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t'appartient pas.", ephemeral=True)
            return
        self.current_page = (self.current_page - 1) % len(self.embed_pages)
        await self.update_message(interaction)

    @ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: Interaction, button: ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t'appartient pas.", ephemeral=True)
            return
        self.current_page = (self.current_page + 1) % len(self.embed_pages)
        await self.update_message(interaction)

################################################################################
# End of File
################################################################################