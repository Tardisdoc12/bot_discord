################################################################################
# filename: bot.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import os

import dotenv
import discord
from discord.ext import commands

from bdd.init_bdd import init_db
from bdd.tags import tag_kind_people,tag_by_channels,channels_for_everyone
from roles.role_base import get_or_create_role

################################################################################

dotenv.load_dotenv()
init_db()

################################################################################
#CONSTANTS:

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire les messages
intents.members = True
id_channel_command = int(os.getenv("ID_CHANNEL_COMMAND"))

message_template = """
Bienvenue à tous sur le serveur **{guild_name}** !

Je suis un bot pour les candidats et les recruteurs.
Je suis le meilleur bot pour vous mettre en contacte.

Vous pouvez cliquer sur un bouton ou les deux selon si vous êtes un recruteur ou un candidat.

Les recruteurs peuvent créer des offres d'emplois et sont les seuls ayant ce pouvoir :\n
\t-Pour créer une offre d'emploi, vous avez la commande: `/create_job_offer`. N'oubliez pas les tags. Ils permettent de mieux accéder aux offres.
\t-Pour supprimer une offre d'emploi, vous avez la commande: `/delete_job`.
\t-Vous pouvez accéder à toutes les offres d'emplois que vous avez publié avec la commande : `get_jobs_from_user` sans aucun argument.
\t-Vous pouvez récupérer un cv d'un utilisateur avec la commande: `/give_resume` + le pseudo de l'utilisateur.

Les candidats ne peuvent que voir les offres d'emplois et mettre leur cv:\n
\t-Pour voir les offres d'emplois d'un utilisateur, vous avez la commande: `/get_jobs_from_user` + le nom du publieur.
\t-Pour voir votre cv, vous avez la commande: `/give_resume` sans aucun pseudo.
\t-Pour mettre votre cv, vous avez la commande: `/send_resume`.
"""
tags_message = """    
Pour commencer à voir les channels qui vous interesse que vous soyez recruteur ou candidat, vous avez la commande: `/create_profile`.
Cette commande vous permet de choisir les tags correspondants à vos compétences et vos connaissances. Vous pourrez aussi mettre toutes les urls que vous souhaitez.
Les tags sont le plus important car ils permettent de mieux vous retrouvez et d'accéder aux channels qui vous interesse. Vous pourrez ainsi avoir les rôles correspondants.

Pour voir les tags, vous avez la commande: `/get_tags`.
Pour voir les tags d'un utilisateur, vous avez la commande: `/get_tags_user` + le pseudo de l'utilisateur.
Pour voir les profils correspondant à un tag, vous avez la commande: `/get_users_name_tag` + le tag.
Si vous avez oublié un tag ou que vous avez mis un tag inutile, pas de panique!
\tPour ajouter un tag, vous avez la commande: `/add_tag` + le tag.
\tPour supprimer un tag, vous avez la commande: `/delete_tag` + le tag.

Pour les urls vous pouvez aussi utiliser la commande: `/get_urls_user` + le pseudo de l'utilisateur. Et ainsi récupérer les urls de quelqu'un.
\tPour modifier une url, vous avez la commande: `/update_urls` + la nouvelle url + l'url originale.
\tPour supprimer une url, vous avez la commande: `/delete_urls` + l'url.
\tPour ajouter une url, vous avez la commande: `/add_urls` + l'url.

Bonne visite et bon courage!
"""

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

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # nécessaire pour lire les messages
        intents.members = True
        self.view_creation_recruteur_candidat = None  # stockage ici
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def setup_hook(self) -> None:

        self.add_view(ViewCreationRecruteurCandidat())
        guild = discord.Object(id=int(GUILD_ID))  # pour test dans un serveur spécifique
        try:
            with open("bdds/message_id.txt", "r") as f:
                message_id = int(f.readline().strip())
                channel = self.get_channel(f.readline().strip())
                if channel:
                    message = await channel.fetch_message(message_id)
                    await message.edit(view=self.view_creation_recruteur_candidat)
        except Exception as e:
            print(f"⚠️ Impossible de recharger la vue persistante : {e}")
        self.tree.copy_global_to(guild=guild)      # copie les commandes globales vers ce serveur
        await self.tree.sync(guild=guild) 

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = PersistentViewBot()

@bot.tree.command(name="generate", description="envoie le message de bienvenue (admin)")
async def send_message_recruteur_candidat(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Tu dois être admin.", ephemeral=True)
        return
    message = message_template.format(guild_name=interaction.guild.name)
    await interaction.response.defer()
    await interaction.followup.send(message)
    sent = await interaction.followup.send(tags_message, view=ViewCreationRecruteurCandidat())
    with open("bdds/message_id.txt","a") as file:
        file.write(str(sent.id) + "\n")
        file.write(str(sent.channel.id) + "\n")

GUILD_ID = int(os.getenv("GUILD_ID"))

################################################################################
# End of File
################################################################################