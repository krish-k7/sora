# discord.py imports
import discord
from discord.ext import commands
from discord import app_commands

# typing imports
from typing import Optional

# misc imports
import requests
from datetime import datetime
from utils.ip import format_ip


# cog
class Util(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


    # application commands
    @app_commands.command(name = 'avatar', description = 'Sends the avatar of the specified user')
    @app_commands.describe(user = 'The user to send the avatar of')
    async def avatar(self, interaction: discord.Interaction, user: Optional[discord.User]) -> None:
        
        user = user or interaction.user
        
        embed = discord.Embed(color = 0x9c7268)
        embed.set_author(name = str(user), icon_url = user.display_avatar)
        embed.set_image(url = user.display_avatar)

        await interaction.response.send_message(embed = embed)


    @app_commands.command(name = 'userinfo', description = 'Sends info about the specified user')
    @app_commands.describe(user = 'The user to send the info of')
    async def userinfo(self, interaction: discord.Interaction, user: Optional[discord.User]) -> None:

        user = user or interaction.user
        created_at = int((user.created_at).timestamp())

        embed = discord.Embed(description = user.mention, color = 0x9c7268, timestamp = datetime.now())
        embed.set_author(name = str(user), icon_url = user.display_avatar)
        embed.add_field(name = 'Registered', value = f'<t:{created_at}:f>', inline = True)
        embed.set_thumbnail(url = user.display_avatar)
        embed.set_footer(text = f'ID: {user.id}')

        await interaction.response.send_message(embed = embed)


    @app_commands.command(name = 'ip', description = 'Sends info about an IP address')
    @app_commands.describe(address = 'IP address', private = 'Make the response only visible to you')
    @app_commands.checks.cooldown(1, 5.0, key = lambda x: x.guild_id)
    async def ip(self, interaction: discord.Interaction, address: str, private: Optional[bool] = False) -> None:
        ip_json = requests.get(f'https://ipwho.is/{address}').json()
        ip_formatted = format_ip(ip_json)
        await interaction.response.send_message(ip_formatted, ephemeral = private)


    @app_commands.command(name = 'purge', description = 'Deletes the specified number of messages from the channel')
    @app_commands.describe(message_count = 'The number of messages to delete')
    @app_commands.rename(message_count = 'amount')
    @app_commands.checks.has_permissions(manage_messages = True)
    async def purge(self, interaction: discord.Interaction, message_count: int) -> None:
        await interaction.response.defer(ephemeral = True)
        await interaction.channel.purge(limit = message_count)
        await interaction.followup.send(f'Purged ``{message_count}`` messages', ephemeral = True)


    # global error handlers
    async def cog_app_command_error(self, interaction: discord.Interaction, error: Exception) -> None:

        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f'Insufficient permissions to run command: ``{interaction.command.name}``', ephemeral = True)


# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Util(bot))
