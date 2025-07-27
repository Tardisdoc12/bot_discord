################################################################################
# filename: event.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 25/07,2025
################################################################################

import discord

from bot import bot, GUILD_ID

################################################################################


@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=discord.Object(id=int(GUILD_ID)))
    await bot.wait_until_ready()
    await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
    print(f"Bot connecté en tant que {bot.user}")


################################################################################
# End of File
################################################################################