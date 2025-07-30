################################################################################
# filename: user_resume.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import os

import discord

from functions.core import (
    extract_content_pdf,
    saving_pdf,
)
from bdd.resume_bdd import (
    get_user_cv_path,
    create_user_cv_path,
    update_user_cv_path,
    get_user_cv_path_from_name,
    verify_user_already_exist,
)

################################################################################

async def download_pdf(interaction: discord.Interaction, file: discord.Attachment):
    #création du dossier
    stockage_pdf_path = "/mount/bdd/pdfs"
    if not os.path.exists(stockage_pdf_path):
        os.mkdir(stockage_pdf_path)

    # gestion de l'attachement
    if file:
        if file.filename.endswith(".pdf"):
            file_bytes = await file.read()
            
            #sauvegarde du fichier
            chemin_complet = os.path.join(stockage_pdf_path, file.filename)
            
            #ajout dans la bdd
            if verify_user_already_exist(interaction.user.id):
                update_user_cv_path(interaction.user.id, chemin_complet)
            else:
                create_user_cv_path(interaction.user.id, chemin_complet)
            
            await saving_pdf(chemin_complet, file, interaction)
            
            #on vérifie si le contenu du pdf est vide
            contenu = extract_content_pdf(file_bytes)
            if contenu:
                await interaction.response.send_message("Le P.D.F. a bien été envoyé")
            else:
                await interaction.response.send_message("Le contenu du PDF est vide.")
        else:
            await interaction.response.send_message("Le fichier attaché n'est pas un PDF.")
    else:
        await interaction.response.send_message("Aucun fichier PDF attaché.")

################################################################################

async def give_resume(interaction: discord.Interaction, user_name : str = None):
    if user_name:
        chemin = get_user_cv_path_from_name(user_name)
        if chemin:
            await interaction.response.send_message(file=discord.File(chemin[0]))
        else:
            await interaction.response.send_message("Aucun fichier PDF attaché.")
    else:
        chemin = get_user_cv_path(interaction.user.id)
        if chemin is not None:
            await interaction.response.send_message(file=discord.File(chemin[0]))
        else:
            await interaction.response.send_message("Aucun fichier PDF attaché.")

################################################################################
# End of File
################################################################################