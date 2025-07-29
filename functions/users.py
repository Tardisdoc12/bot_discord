################################################################################
# filename: users.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import discord

from bdd.users import (
    get_user_name_from_user_id,
    add_user,
    get_user_id_from_user_name,
    verify_user_already_exist,
    update_profil_user,
    get_profil_already_created
)

################################################################################

def is_creating_profil(interaction: discord.Interaction) -> bool:
    if get_profil_already_created(interaction.user.id):
        return False
    update_profil_user(interaction.user.id)
    return True

################################################################################

def get_user_id(user_name: str) -> int:
    return get_user_id_from_user_name(user_name)

################################################################################

def get_members(interaction: discord.Interaction) -> list:
    members = interaction.guild.members
    return members

################################################################################

def register_members(interaction: discord.Interaction) -> list:
    members = get_members(interaction)
    for member in members:
        add_user(member.id, member.name)
    return members

################################################################################

def miss_profil(interaction: discord.Interaction) -> bool:
    if verify_user_already_exist(interaction.user.id) and get_profil_already_created(interaction.user.id):
        return False
    return True
        

################################################################################

def register_member(interaction: discord.Interaction) -> bool:
    if verify_user_already_exist(interaction.user.id):
        return False
    add_user(interaction.user.id, interaction.user.name)
    return True

################################################################################

def get_user_name(user_id: int) -> str:
    return get_user_name_from_user_id(user_id)

################################################################################
# End of File
################################################################################