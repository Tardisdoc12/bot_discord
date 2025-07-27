################################################################################
# filename: role_base.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 26/07,2025
################################################################################

import discord
import re

from bdd.tags import category_recrutement

################################################################################

async def create_role_base(name_role, guild, couleur, salons = []):
    role = discord.utils.get(guild.roles, name=name_role)
    if role is None:
        role = await guild.create_role(
            name=name_role,
            colour=couleur,
            permissions=discord.Permissions.none(),
            reason=f"Rôle {name_role} créé automatiquement"
        )
        for channel in guild.channels:
            overwrite = channel.overwrites_for(role)
            if channel.name.lower() in salons:
                overwrite.view_channel = True
                if isinstance(channel, discord.TextChannel):
                    overwrite.send_messages = True
                elif isinstance(channel, discord.VoiceChannel):
                    overwrite.connect = True
                    overwrite.speak = True
            else:
                # Bloquer l'accès
                overwrite.view_channel = False
                overwrite.send_messages = False
                overwrite.connect = False
            try:
                await channel.set_permissions(role, overwrite=overwrite)
            except:
                raise Exception(f"Impossible de donner les permissions au role {role.name} sur le salon {channel.name}")
    return role

################################################################################

async def get_or_create_role(tag: str, guild: discord.Guild, default_color=discord.Colour.green(),salons =[]) -> discord.Role:
    # Cherche un rôle existant avec un nom contenant le tag
    for role in guild.roles:
        if tag.lower() in role.name.lower():
            return role  # Le rôle existe déjà
    
    role = await create_role_base(tag, guild, default_color,salons=salons)
    return role

################################################################################

async def add_role_to_member(member, role):
    return await member.add_roles(role)

################################################################################

def get_colour_from_rgb(r, g, b):
    return discord.Color.from_rgb(r, g, b)

################################################################################

def remove_role_from_member(member, role):
    return member.remove_roles(role)
################################################################################

def remove_emoji(string):
    return re.sub(r"[^\w+]","",string)

################################################################################

def callback(channel : discord.TextChannel)-> bool:
    return remove_emoji(channel.name).lower().strip().endswith("recrutement")

async def get_or_create_channel(guild : discord.Guild, channel_name : str,role : discord.Role) -> discord.TextChannel:

    category = discord.utils.find(
        callback,
        guild.categories
    )
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role: discord.PermissionOverwrite(view_channel=True)
    }

    name_channel_without_emoji = remove_emoji(channel_name.lower())
    existing_channel = next(
        (c for c in guild.channels if name_channel_without_emoji in c.name),
        None
    )
    if existing_channel:
        return existing_channel
    else:
        channel_text = await guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category)
        return channel_text

################################################################################
# End of File
################################################################################