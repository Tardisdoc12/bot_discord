################################################################################
# filename: core.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################
#IMPORTS

import PyPDF2
import io
import discord

################################################################################

def check_channel_id(ctx, id_channel_command):
    if ctx.channel.id != id_channel_command:
        return False
    return True

################################################################################

def extract_content_pdf(bites_file):
    reader = PyPDF2.PdfReader(io.BytesIO(bites_file))
    contenu = ""
    for page in reader.pages:
        contenu += page.extract_text() or ""
    return contenu

################################################################################

async def saving_pdf(chemin_complet, attachment, interaction : discord.Interaction):
    file_bytes = await attachment.read()
    with open(chemin_complet, "wb") as f:
        f.write(file_bytes)

################################################################################
# End of File
################################################################################