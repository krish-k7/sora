# discord.py imports
import discord
from discord.ext import commands
from discord import app_commands

# misc imports
import time


# cog
class Info(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


    # application commands
    @app_commands.command(name = 'ping', description = 'Send the bot\'s latency')
    async def ping(self, interaction: discord.Interaction) -> None:
        before = time.monotonic()
        await interaction.response.send_message(f'Ping?')
        after = round((time.monotonic() - before) * 1000)
        await interaction.edit_original_response(content = f'Pong! ``{after}ms``')


# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))