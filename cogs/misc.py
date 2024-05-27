# discord.py imports
import discord
from discord.ext import commands
from discord import app_commands

# ui imports
from ui.views import CatView, DogView

# misc imports
import requests


# cog
class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot


    # application commands
    @app_commands.command(name = 'cat', description = 'Sends a random cat image')
    async def cat(self, interaction: discord.Interaction):
        
        def fetch_image() -> discord.Embed:
            image = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=jpg,png').json()[0]['url']
            embed = discord.Embed(color = 0x9c7268)
            embed.set_image(url = image)
            return embed
        
        await interaction.response.send_message(embed = fetch_image(), view = CatView(fetch_image))

    
    @app_commands.command(name = 'dog', description = 'Sends a random dog image')
    async def dog(self, interaction: discord.Interaction):

        def fetch_image() -> discord.Embed:
            image = requests.get('https://api.thedogapi.com/v1/images/search?mime_types=jpg,png').json()[0]['url']
            embed = discord.Embed(color = 0x9c7268)
            embed.set_image(url = image)
            return embed
        
        await interaction.response.send_message(embed = fetch_image(), view = DogView(fetch_image))


# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))