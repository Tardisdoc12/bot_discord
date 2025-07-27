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
from bdd.tags import all_tags, tag_by_channels, channels_for_everyone, tag_kind_people

################################################################################

admin = app_commands.Group(name="admin", description="Commandes admin")
bot.tree.add_command(admin)

################################################################################

@admin.command(name="create_all_roles", description="Créer tous les roles", extras = {"default_member_permissions":(Permissions(administrator=True))})
async def create_all_roles(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Tu dois être admin.", ephemeral=True)
        return
    
    role_to_create = all_tags + tag_kind_people
    await interaction.response.defer(ephemeral=True) 
    channel_created = []
    for tag in role_to_create:
        names_channel = tag_by_channels.get(tag,[])
        salons_autorise = channels_for_everyone + names_channel
        role = await get_or_create_role(tag, interaction.guild, discord.Colour.green(), salons=salons_autorise)
        for name_channel in names_channel:
            if name_channel not in channel_created:
                channel_created.append(name_channel)
                await get_or_create_channel(interaction.guild, name_channel, role)

    await interaction.followup.send("✅ Tous les rôles ont été créés.")

################################################################################

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Tu n'as pas le rôle requis pour cette commande.", ephemeral=True)

################################################################################
# End of File
################################################################################