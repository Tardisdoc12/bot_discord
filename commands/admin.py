################################################################################
# filename: admin.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 27/07,2025
################################################################################

import discord
from discord import Permissions,app_commands

from bot import bot
from roles.role_base import get_or_create_role, get_or_create_channel
from bdd.tags import all_tags, tag_by_channels, channels_for_everyone

################################################################################

admin = app_commands.Group(name="admin", description="Commandes admin")
bot.tree.add_command(admin)

################################################################################

@admin.command(name="create_all_roles", description="Créer tous les roles", extras = {"default_member_permissions":(Permissions(administrator=True))})
async def create_all_roles(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Tu dois être admin.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True) 
    
    for tag in all_tags:
        names_channel = tag_by_channels.get(tag,[])
        salons_autorise = channels_for_everyone + names_channel
        role = await get_or_create_role(tag, interaction.guild, discord.Colour.green(), salons=salons_autorise)
        for name_channel in names_channel:
            await get_or_create_channel(interaction.guild, name_channel, role)

    await interaction.followup.send("✅ Tous les rôles ont été créés.")

################################################################################
# End of File
################################################################################