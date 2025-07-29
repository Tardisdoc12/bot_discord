################################################################################
# filename: test.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord
from discord import app_commands

from bot import bot
from bdd.tags import all_tags, tag_kind_people
from functions.tags_jobs import add_tag_to_job, delete_all_tags_from_job, get_jobs_from_tag
from functions.temp_stockage import temp_data
from functions.jobs import (
    create_job, get_job_id,
    get_job_informations,
    delete_job_by_id,
    get_all_jobs_user_name,
    get_user_from_job_id
)
from bdd.tags_jobs import all_tags_job
from functions.jobs_card import create_job_card
from functions.users import get_user_name,miss_profil,get_user_id
from functions.paginations_embed import EmbedPaginator
from functions.view_creation_base import ViewCreationBase
from functions.core import has_role, EmptyView

################################################################################

class PostulationButton(discord.ui.Button):

    def __init__(self, job_id, recruter_id, candidate_id):
        super().__init__(label="Postuler", style=discord.ButtonStyle.primary)
        self.job_id = job_id
        self.recruter_id = recruter_id
        self.candidate_id = candidate_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.candidate_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return
        recruter_member = interaction.guild.get_member(self.recruter_id)
        try:
            await recruter_member.send(
                f"**{interaction.user.name}** a postuler pour l'offre {self.job_id}.\nSi vous souhiatez vous pouvez récupérer son cv via la commande /get_cv {interaction.user.name}.\nBonne journée!"
            )
        except discord.errors.Forbidden:
            await interaction.response.send_message("Ce recruteur doit être contacter directement par vos soins.", ephemeral=True)
            return
        await interaction.response.send_message("Vous avez postuler pour cette offre.", ephemeral=True)

################################################################################

class JobOfferView(ViewCreationBase):
    def __init__(self, user_id):
        super().__init__(user_id=user_id)

    @discord.ui.button(label="Publier l’offre", style=discord.ButtonStyle.success)
    async def publish(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Ce menu ne t’appartient pas.", ephemeral=True)
            return

        data = temp_data.pop(self.user_id, None)
        if not data:
            await interaction.response.send_message("Aucune donnée trouvée.", ephemeral=True)
            return

        job_id = get_job_id(data["title"], data["description"], data["company"], data["url"], interaction.user.id)
        if job_id is not None:
            await interaction.response.send_message("Une offre avec ces informations existe deja. elle a l'id {job_id}", ephemeral=True)
            return
        create_job(data["title"], data["company"], data["description"], data["url"], interaction.user.id, data["salaire"], data["horaires"])
        job_id = get_job_id(data["title"], data["description"], data["company"], data["url"], interaction.user.id)[0]

        for tag in data.get("tags", []):
            add_tag_to_job(tag,job_id)
        tags_job = ", ".join(data.get("tags", [])) or "Aucun"
        
        user_name = interaction.user.name
        embed_job = create_job_card(
            data["title"],
            job_id,
            data["description"],
            tags_job,
            data["url"],
            data["company"],
            data["salaire"],
            data["horaires"],
            user_name
        )
        await interaction.channel.send( "📝 Offre publiée", embed=embed_job)

################################################################################

class JobPostulatePaginator(discord.ui.View):
    def __init__(self, embeds: list, recruters_id: list, candidate_id: int, jobs_id: list):
        super().__init__(timeout=None)
        self.rectuters_id = recruters_id
        self.candidate_id = candidate_id
        self.jobs_id = jobs_id
        self.embeds = embeds
        self.current_page = 0
        self.add_item(
            PostulationButton(
                job_id = self.jobs_id[self.current_page],
                recruter_id = self.rectuters_id[self.current_page],
                candidate_id = self.candidate_id
            )
        )
    
    async def update_message(self, interaction: discord.Interaction):
        embed = self.embeds[self.current_page]
        for button in self.children:
            if isinstance(button, PostulationButton):
                button.job_id = self.jobs_id[self.current_page]
                button.recruter_id = self.rectuters_id[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.embeds)
        await self.update_message(interaction)
    
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.embeds)
        await self.update_message(interaction)

################################################################################

@has_role(tag_kind_people[0])
@bot.tree.command(name="create_job_offer", description="Créer une offre avec tags interactifs")
@app_commands.describe(title="Titre", description="Description", url="Lien", company="Entreprise")
async def create_job_offer(interaction: discord.Interaction, title: str, description: str, url: str, company: str, salaire: str = None, horaires: str = None):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    temp_data[interaction.user.id] = {
        "title": title,
        "description": description,
        "url": url,
        "company": company,
        "salaire": salaire,
        "horaires": horaires,
        "tags": []
    }

    view = JobOfferView(interaction.user.id)
    await interaction.response.send_message(
        f"📝 Offre initialisée pour **{title}** chez **{company}**.\n"
        f"Ajoute des tags ou publie directement.",
        view=view,
        ephemeral=True
    )

################################################################################

@bot.tree.command(name="get_job", description="Rechercher une offre")
async def get_job_from_id(interaction: discord.Interaction, job_id : int):
    if miss_profil(interaction):
        await interaction.response.send_message("Vous devez créer un profile avec la commande /create_profile",ephemeral=True)
        return
    job = get_job_informations(job_id)
    if job is None:
        await interaction.response.send_message("Aucune offre trouvée.", ephemeral=True)
        return
    job_id, title, company, description, url, salaire, horaires, user_id = job
    tags_job = all_tags_job(job_id)
    if tags_job == []:
        tags_job = "Aucun"
    else:
        tags_job = ",\n".join(tags_job)

    user_name = get_user_name(user_id)[0]

    embed_job = create_job_card(title, job_id, description, tags_job, url, company, salaire, horaires, user_name)

    if int(user_id) != interaction.user.id:
        view = EmptyView(recruter_id = user_id, job_id = job_id, candidate_id = interaction.user.id)
        view.add_item(PostulationButton(recruter_id = user_id, job_id = job_id, candidate_id = interaction.user.id))
        await interaction.response.send_message(
            embed=embed_job,
            view=view
        )
        return
    await interaction.response.send_message(
        embed=embed_job
    )


################################################################################

@has_role(tag_kind_people[0])
@bot.tree.command(name="delete_job", description="Supprime une offre")
async def delete_job_with_id(interaction: discord.Interaction, job_id : int):
    user_id = get_user_from_job_id(job_id)
    if int(user_id) != interaction.user.id:
        await interaction.response.send_message("Cette offre ne t’appartient pas.", ephemeral=True)
        return
    delete_job_by_id(job_id)
    delete_all_tags_from_job(job_id)
    await interaction.response.send_message("Offre supprimée.")

################################################################################

@bot.tree.command(name="get_jobs_from_tag", description="Rechercher des offres par tag")
async def get_jobs_tag(interaction: discord.Interaction, tag : str):
    jobs = get_jobs_from_tag(tag)
    if jobs == []:
        await interaction.response.send_message("Aucune offre trouvée.", ephemeral=True)
        return
    
    embeds_pages = []
    recruters_id = []
    jobs_id = []
    for job in jobs:
        job_id, title, company, description, user_id, url, salaire, horaires = job
        tags_job = all_tags_job(job_id)
        if tags_job == []:
            tags_job = "Aucun"
        else:
            tags_job = ",\n".join(tags_job)

        user_name = get_user_name(user_id)[0]
        recruters_id.append(int(user_id))
        jobs_id.append(int(job_id))
        embed_job = create_job_card(title, job_id, description, tags_job, url, company, salaire, horaires, user_name)
        embeds_pages.append(embed_job)
    
    embeds_paginator = JobPostulatePaginator(
        embeds = embeds_pages,
        recruters_id = recruters_id,
        candidate_id = interaction.user.id,
        jobs_id = jobs_id
    )
    
    await interaction.response.send_message(embed=embeds_pages[0], view=embeds_paginator)

################################################################################

@bot.tree.command(name="get_jobs_from_user", description="Rechercher des offres par utilisateur")
async def get_jobs_from_user(interaction: discord.Interaction, user_name : str = None):
    user = user_name if user_name else interaction.user.name
    jobs = get_all_jobs_user_name(user)

    if jobs == []:
        await interaction.response.send_message("Aucune offre trouvée.", ephemeral=True)
        return
    embeds_pages = []
    
    for job in jobs:
        job_id, title, company, description, url, salaire, horaires = job
        tags_job = all_tags_job(job_id)
        if tags_job == []:
            tags_job = "Aucun"
        else:
            tags_job = ",\n".join(tags_job)

        embed_job = create_job_card(title, job_id, description, tags_job, url, company, salaire, horaires, user)
        embeds_pages.append(embed_job)
    embeds_paginator = EmbedPaginator(interaction.user.id, embeds_pages)
    recruter_id = get_user_id(user)
    if recruter_id is None:
        await interaction.response.send_message("Problème dans la base de données. Il y a une offre sans recruteur.", ephemeral=True)
        return
    if recruter_id != interaction.user.id:
        embeds_paginator.add_item(
            PostulationButton(
                recruter_id = recruter_id,
                job_id = job_id,
                candidate_id = interaction.user.id
            )
        )
    
    await interaction.response.send_message(embed=embeds_pages[0], view=embeds_paginator)

################################################################################

@get_jobs_from_user.autocomplete("user_name")
async def nom_autocomplete(interaction: discord.Interaction, current: str):

    all_names = interaction.guild.fetch_members(limit=None)

    filtered = sorted(
        [member.name async for member in all_names if current.lower() in member.display_name.lower()],
        key=lambda x: x.lower().find(current.lower())
    )[:25]

    users_name = [app_commands.Choice(name=member_name, value=member_name) for member_name in filtered]
    
    return users_name

################################################################################

@get_jobs_tag.autocomplete("tag")
async def name_tags(interaction: discord.Interaction, current_input : str):
    tags_name = []

    # Liste de tous les tags possibles (ex: récupérés depuis ta base de données ou en mémoire)
    tags  = all_tags # Assure-toi que `tags` est une liste accessible ici

    # Filtrage intelligent : on garde les tags contenant la saisie (insensible à la casse)
    filtered = sorted(
        [tag for tag in tags if current_input.lower() in tag.lower()],
        key=lambda x: x.lower().find(current_input.lower())
    )

    # Limite à 25 suggestions max
    filtered = filtered[:25]

    # Création des objets Choice
    tags_name = [app_commands.Choice(name=tag, value=tag) for tag in filtered]

    return tags_name

################################################################################
# End of File
################################################################################