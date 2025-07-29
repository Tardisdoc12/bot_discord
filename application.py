################################################################################
# filename: routes.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import os
from bot import bot
import commands.profile
import commands.resume
import commands.tags_user
import commands.urls
import commands.jobs_offer
import commands.admin
import commands.city


bot.run(os.getenv("TOKEN_BOT"))

################################################################################
# End of File
################################################################################