################################################################################
# filename: admin.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 27/07,2025
################################################################################

import os

import discord
from discord import Permissions,app_commands

from bot import bot
from roles.role_base import get_or_create_role, get_or_create_channel
from bdd.tags import all_tags, tag_by_channels, channels_for_everyone, tag_kind_people
from functions.view_recuteur_candidat import ViewCreationRecruteurCandidat
from functions.migrations import migration_data

################################################################################

admin = app_commands.Group(name="admin", description="Commandes admin")
bot.tree.add_command(admin)

################################################################################

message_template = """
Bienvenue à tous sur le serveur **{guild_name}** !

Je suis un bot pour les candidats et les recruteurs.
Je suis le meilleur bot pour vous mettre en contact.

Vous pouvez cliquer sur un bouton ou les deux selon si vous êtes un recruteur ou un candidat.

:white_check_mark: Les recruteurs peuvent créer des offres d'emplois et sont les seuls ayant ce pouvoir :\n
\t▶️ -Pour créer une offre d'emploi, vous avez la commande: `/create_job_offer`. N'oubliez pas les tags. Ils permettent de mieux accéder aux offres.
\t▶️ -Pour supprimer une offre d'emploi, vous avez la commande: `/delete_job`.
\t▶️ -Vous pouvez accéder à toutes les offres d'emplois que vous avez publié avec la commande : `get_jobs_from_user` sans aucun argument.
\t▶️ -Vous pouvez récupérer un cv d'un utilisateur avec la commande: `/give_resume` + le pseudo de l'utilisateur.

:white_check_mark: Les candidats ne peuvent que voir les offres d'emplois et mettre leur cv:\n
\t▶️ -Pour voir les offres d'emplois d'un utilisateur, vous avez la commande: `/get_jobs_from_user` + le nom du publieur.
\t▶️ -Pour voir votre cv, vous avez la commande: `/give_resume` sans aucun pseudo.
\t▶️ -Pour mettre votre cv, vous avez la commande: `/send_resume`.
"""
tags_message = """
:white_check_mark: Pour commencer à voir les channels qui vous interesse que vous soyez recruteur ou candidat, vous avez la commande: `/create_profile`.
Cette commande vous permet de choisir les tags correspondants à vos compétences et vos connaissances. Vous pourrez aussi mettre toutes les urls que vous souhaitez.
Les tags sont le plus important car ils permettent de mieux vous retrouvez et d'accéder aux channels qui vous interesse. Vous pourrez ainsi avoir les rôles correspondants.

:white_check_mark: Pour voir les tags, vous avez la commande: `/get_tags`.
Pour voir les tags d'un utilisateur, vous avez la commande: `/get_tags_user` + le pseudo de l'utilisateur.
Pour voir les profils correspondant à un tag, vous avez la commande: `/get_users_name_tag` + le tag.
Si vous avez oublié un tag ou que vous avez mis un tag inutile, pas de panique!
\t▶️ Pour ajouter un tag, vous avez la commande: `/add_tag` + le tag.
\t▶️ Pour supprimer un tag, vous avez la commande: `/delete_tag` + le tag.

:white_check_mark: Pour les urls vous pouvez aussi utiliser la commande: `/get_urls_user` + le pseudo de l'utilisateur. Et ainsi récupérer les urls de quelqu'un.
\t▶️ Pour modifier une url, vous avez la commande: `/update_urls` + la nouvelle url + l'url originale.
\t▶️ Pour supprimer une url, vous avez la commande: `/delete_urls` + l'url.
\t▶️ Pour ajouter une url, vous avez la commande: `/add_urls` + l'url.

Bonne visite et bon courage!
"""

################################################################################

@admin.command(name="create_all_roles", description="Créer tous les roles(admin)", extras = {"default_member_permissions":(Permissions(administrator=True))})
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

@bot.tree.command(name="generate", description="envoie le message de bienvenue (admin)")
async def send_message_recruteur_candidat(interaction: discord.Interaction, id_channel: str = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Tu dois être admin.", ephemeral=True)
        return
    message = message_template.format(guild_name=interaction.guild.name)
    
    # Recuperation du channel
    target_channel_id = int(id_channel) if id_channel else interaction.channel_id
    channel = interaction.client.get_channel(target_channel_id)
    if channel is None:
        channel = await interaction.client.fetch_channel(target_channel_id)
    
    # Envoie du message
    await interaction.response.defer()
    await channel.send(message)
    sent = await channel.send(tags_message, view=ViewCreationRecruteurCandidat())
    await interaction.followup.send("✅ Message envoyé.",ephemeral=True)
    # Sauvegarde de l'id du message et du channel
    with open("/mount/bdd/message_id.txt","w") as file:
        file.write(str(sent.id) + "\n")
        if id_channel:
            file.write(str(id_channel) + "\n")
        else:
            file.write(str(sent.channel.id) + "\n")

################################################################################

@bot.tree.command(name="migration", description="Migration des données d'un utilisateur vers un autre (admin)")
async def migration(interaction: discord.Interaction, user_id: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Tu dois être admin.", ephemeral=True)
        return
    user = await bot.fetch_user(user_id)
    response = await migration_data(interaction.user.name, user_id, user.name)
    if response["success"]:
        interaction.followup.send(response.message,ephemeral=True)
    else:
        interaction.followup.send(response.message,ephemeral=True)

################################################################################

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Tu n'as pas le rôle requis pour cette commande.", ephemeral=True)

################################################################################
# End of File
################################################################################