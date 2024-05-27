# discord.py imports
import discord
import discord.ui

# misc imports
from typing import Callable

# cat command view
class CatView(discord.ui.View):

    def __init__(self, func: Callable[[], discord.Embed]) -> None:
        super().__init__(timeout = 300)
        self.func = func


    @discord.ui.button(label = 'Another', style = discord.ButtonStyle.gray, emoji = '🐱')
    async def send_cat_image(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send(embed = self.func(), view = CatView(self.func))


class DogView(discord.ui.View):

    def __init__(self, func: Callable[[], discord.Embed]) -> None:
        super().__init__(timeout = 300)
        self.func = func


    @discord.ui.button(label = 'Another', style = discord.ButtonStyle.gray, emoji = '🐶')
    async def send_dog_image(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view = self)
        await interaction.followup.send(embed = self.func(), view = DogView(self.func))