################################################################################
# filename: card_job.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import discord

from bdd.jobs import get_job_from_id
from functions.tags_jobs import all_tags_job

################################################################################

def create_embed_jobs(title : str, description : str, tags : list, url : str, company : str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.teal()
    )
    embed.add_field(name="Tags:", value="\n".join(tags), inline=True)
    embed.add_field(name="Url:", value=url, inline=True)
    embed.add_field(name="Company:", value=company, inline=True)
    return embed

################################################################################

def prepare_embed(job_id : int) -> discord.Embed:
    title, description, url, company = get_job_from_id(job_id)
    tags = all_tags_job(job_id)
    return create_embed_jobs(title, description, tags, url, company)

################################################################################
# End of File
################################################################################