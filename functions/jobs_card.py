################################################################################
# filename: jobs_card.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord

################################################################################

def create_job_card(title, job_id, description, tags, url, company, salaire, horaires, user_name):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.add_field(name="ID:", value=job_id, inline=True)
    embed.add_field(name="Lien:", value=url, inline=True)
    embed.add_field(name="Entreprise:", value=company, inline=True)
    embed.add_field(name="Auteur:", value=user_name, inline=True)
    embed.add_field(name="Salaire:", value=salaire, inline=True)
    embed.add_field(name="Horaires:", value=horaires, inline=True)
    embed.add_field(name="Tags:", value=tags, inline=True)
    return embed

################################################################################
# End of File
################################################################################