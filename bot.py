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
from functions.view_recuteur_candidat import ViewCreationRecruteurCandidat

################################################################################

dotenv.load_dotenv()
init_db()

################################################################################
#CONSTANTS:

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire les messages
intents.members = True
id_channel_command = [int(channel) for channel in os.getenv("ID_CHANNEL_COMMAND").split(',')]

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
        if os.path.exists("bdds/message_id.txt"):
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
        await self.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = PersistentViewBot()

GUILD_ID = int(os.getenv("GUILD_ID"))

################################################################################
# End of File
################################################################################