# discord.py imports
import discord
from discord.ext import commands
from discord import app_commands


# cog
class Events(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


    # event listeners
    @commands.Cog.listener()
    async def on_message(self, message):
        # add event handler here if needed
        pass



# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))