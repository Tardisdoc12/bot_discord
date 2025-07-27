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
from functions.users import register_member,is_creating_profil,miss_profil
from functions.profil_user import create_profile, get_profil_photo_user_name, get_profil
from functions.temp_stockage import temp_data
from functions.tags_users import get_informations_from_username
from functions.view_creation_base import ViewCreationBase
from functions.urls import create_url
from bdd.tags_users_bdd import add_tag_to_user,get_users_from_tag
from bdd.tags import all_tags, tag_by_channels, channels_for_everyone
from functions.paginations_embed import EmbedPaginator
from roles.role_base import add_role_to_member, get_or_create_channel, get_or_create_role

################################################################################

class UserProfileView(ViewCreationBase):
    def __init__(self, user_id):
        super().__init__(user_id=user_id, timeout=None)

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

        for url in data.get("urls", []):
            create_url(interaction.user.id, url)
        
        member = interaction.guild.get_member(interaction.user.id)
        tags = list(set(data.get("tags", [])))
        for tag in tags:    
            add_tag_to_user(member.id, tag)
            names_channel = tag_by_channels.get(tag,[])
            salons_autorise = channels_for_everyone + names_channel
            role = await get_or_create_role(tag, interaction.guild, discord.Colour.green(),salons=salons_autorise)
            if role not in member.roles:
                await add_role_to_member(member, role)

        photo = await get_profil_photo_user_name(member.name, interaction)
        profil_embed = get_profil(
            interaction.user.name,
            data.get("tags",[]),
            data.get("urls",[]),
            photo
        )

        await interaction.response.send_message("Profil créer :",embed=profil_embed,ephemeral=True)

################################################################################

@bot.tree.command(name="get_profile", description="Donne le profil de l'utilisateur")
async def get_profile(interaction: discord.Interaction, user_name : str = None) -> str:
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
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
    )[:25]

    users_name = [app_commands.Choice(name=member_name, value=member_name) for member_name in filtered]
    
    return users_name

################################################################################

@bot.tree.command(name="create_profile", description="Créer le profile de l'utilisateur")
async def create_profile_user(interaction: discord.Interaction):
    register_member(interaction)
    if not is_creating_profil(interaction):
        await interaction.response.send_message("Vous avez deja un profile.",ephemeral=True)
        return
    if not check_channel_id(interaction, id_channel_command):
        return
    await interaction.response.send_message("Créer le profile", view=UserProfileView(interaction.user.id), ephemeral=True)

################################################################################

@bot.tree.command(name="get_users_from_tag", description="Donne tous les utilisateurs ayant un tag")
async def get_users_name_tag(interaction: discord.Interaction, tag : str) -> list:
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    users = get_users_from_tag(tag)
    if not users:
        await interaction.response.send_message("Aucun utilisateur n'a ce tag.")
    else:
        users_embed = []
        for user_name in users:
            _, tags, urls = get_informations_from_username(user_name)
            photo = await get_profil_photo_user_name(user_name, interaction)
            embed_profil = get_profil(user_name, tags, urls, photo)
            users_embed.append(embed_profil)
        embeds_paginator = EmbedPaginator(interaction.user.id, users_embed)
        await interaction.response.send_message(embed=users_embed[0], view=embeds_paginator, ephemeral=True)

################################################################################

@get_users_name_tag.autocomplete("tag")
async def tag_autocomplete(interaction: discord.Interaction, current: str):
    tags = all_tags
    filtered = sorted(
        [tag for tag in tags if current.lower() in tag.lower()],
        key=lambda x: x.lower().find(current.lower())
    )[:25]
    tags_user = [app_commands.Choice(name=tag, value=tag) for tag in filtered]
    return tags_user

################################################################################
# End of File
################################################################################