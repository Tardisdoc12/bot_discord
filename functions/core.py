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

from functions.temp_stockage import temp_data

################################################################################

async def check_channel_id(interaction : discord.Interaction, id_channel_command : int|list[int]):
    if isinstance(id_channel_command, int):
        id_channel_command = [id_channel_command]
    if not interaction.channel.id in id_channel_command:
            await interaction.response.send_message("Vous devez utiliser cette commande dans les salons autorisés",ephemeral=True)
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

class TagSelectView(discord.ui.View):
    def __init__(self, user_id, tags_to_select, placeholder, message_success = f"✅ Tag enregistré avec succée!"):
        super().__init__(timeout=60)
        self.user_id = user_id

        options = [discord.SelectOption(label=tag) for tag in tags_to_select]
        self.select = discord.ui.Select(placeholder=placeholder, options=options, min_values=1, max_values=1)
        self.select.callback = self.on_select
        self.message_success = message_success
        self.add_item(self.select)

    async def on_select(self, interaction: discord.Interaction):
        tag_value = self.select.values[0]
        user_data = temp_data.get(self.user_id, {})
        user_data.setdefault("tags", []).append(tag_value)
        temp_data[self.user_id] = user_data
        if self.message_success:
            await interaction.response.send_message(self.message_success, ephemeral=True)
        else:
            await interaction.response.send_message(f"✅ Tag sélectionné : **{tag_value}**", ephemeral=True)

################################################################################

class UrlModal(discord.ui.Modal, title="Ajouter une URL"):
    url = discord.ui.TextInput(label="URL", placeholder="ex: https://mon-site.com", required=True)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        url_value = self.url.value.strip()
        user_data = temp_data.get(self.user_id, {})
        user_data.setdefault("urls", []).append(url_value)
        temp_data[self.user_id] = user_data

        await interaction.response.send_message(f"✅ URL ajoutée : **{url_value}**", ephemeral=True)

################################################################################

def has_role(role_name: str):
    async def predicate(interaction: discord.Interaction) -> bool:
        return any(role.name == role_name for role in interaction.user.roles)
    return discord.app_commands.check(predicate)

################################################################################
# End of File
################################################################################