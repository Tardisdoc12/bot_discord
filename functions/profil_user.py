################################################################################
# filename: profil_user.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import discord

from bdd.urls import (
    get_urls_from_user_name,
    get_urls_from_user_id
)
from functions.tags_users import get_tags_from_user_id_or_name
from functions.city_user import get_city_from_user_id
from bdd.users import get_user_name_from_user_id

################################################################################

def get_profil(user_name : str, tags : list, urls : list,city : list , photo : str) -> str:
    discord_embed = discord.Embed(
        title=f"📋 Profil de {user_name}",
        color=discord.Color.teal()
    )
    if tags != []:
        discord_embed.add_field(name="Tags:", value="\n".join(tags), inline=True)
    if urls != []:
        discord_embed.add_field(name="Urls:", value="\n".join(urls), inline=True)
    if city != []:
        discord_embed.add_field(name="Ville:", value="\n".join(city), inline=True)
    discord_embed.set_thumbnail(url=photo)
    return discord_embed

################################################################################

async def get_profil_photo_user_name(user_name : str, interaction: discord.Interaction) -> str:
    guild = interaction.guild

    member = discord.utils.find(
        lambda m: m.name.lower() == user_name.lower() or m.display_name.lower() == user_name.lower(),
        guild.members
    )

    if not member:
        await interaction.response.send_message(f"Utilisateur '{user_name}' introuvable.")
        return

    # Récupérer l'URL de l'avatar
    return member.avatar.url if member.avatar else member.default_avatar.url

################################################################################

async def create_profile(user_name : str, interaction: discord.Interaction) -> str:
    tags = get_tags_from_user_id_or_name(user_name)
    if user_name is None:
        user = interaction.user
        user_name = get_user_name_from_user_id(user.id)
        if user_name is None:
            return None
        user_name = user_name[0]
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        urls = get_urls_from_user_id(user.id)
    else:
        urls = get_urls_from_user_name(user_name)
        avatar_url = await get_profil_photo_user_name(user_name, interaction)
    if urls:
        urls = [url[0] for url in urls if url is not None]
    else:
        urls = []
    cities = get_city_from_user_id(user_id=user.id)
    return get_profil(user_name, tags if tags else [], urls, cities, avatar_url)

################################################################################
# End of File
################################################################################