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

################################################################################

dotenv.load_dotenv()
init_db()

################################################################################
#CONSTANTS:

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire les messages
intents.members = True
id_channel_command = int(os.getenv("ID_CHANNEL_COMMAND"))

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = int(os.getenv("GUILD_ID"))

################################################################################
# End of File
################################################################################