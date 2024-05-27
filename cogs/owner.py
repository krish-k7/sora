# discord.py imports
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

# typing imports
from typing import Optional

# misc imports
import os
import io
import asyncio
import textwrap
import traceback
import contextlib
from aioconsole import aexec
from colorama import Fore, Style


# variables
cog_choices = [
    Choice(name = cog_name[:-3], value = cog_name[:-3]) for cog_name in os.listdir('./cogs') if cog_name.endswith('.py')
]


# functions
def uncodeblock(content: str) -> str:

    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    else:
        return content


# slash command checks
def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == interaction.client.owner_id


# cog
class Owner(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


    # text commands
    @commands.command(name = 'eval', description = 'Evaluates Python code', aliases = ['e'])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, code: str) -> None:

        env = {
            'discord': discord,
            'commands': commands,
            'bot': self.bot,
            'ctx': ctx,
            'asyncio': asyncio,
            'sleep': asyncio.sleep,
            'os': os,
            'io': io
        }

        code: str = uncodeblock(code)

        async with ctx.typing():
            with io.StringIO() as stdout:
                with contextlib.redirect_stdout(stdout):

                    try:
                        await aexec(source = 'async def func():\n' + textwrap.indent(code, '    '), local = env)
                        await env['func']()
                        output = stdout.getvalue()

                        if output:

                            if len(output) + 10 > 2000:
                                file = io.StringIO(output)
                                await ctx.reply(file = discord.File(file, filename = 'output.txt'))
                                
                            else:
                                await ctx.reply(f'```{output}```')

                        else:
                            await ctx.reply('Executed with no output')

                    except Exception:
                        output = traceback.format_exc()
                        await ctx.reply(f'```ansi\n{Fore.RED + output + Style.RESET_ALL}```')
    
    
    @commands.command(name = 'clear', description = 'Clears the console')
    @commands.is_owner()
    async def clear(self, ctx: commands.Context) -> None:
        
        if os.name == 'nt':
            os.system('cls')
        
        else:
            os.system('clear')

        await ctx.message.add_reaction('✅')

    
    # application commands
    @app_commands.command(name = 'load', description = 'Loads a cog')
    @app_commands.describe(cog = 'The cog to load')
    @app_commands.choices(cog = cog_choices)
    @app_commands.check(is_owner)
    async def load(self, interaction: discord.Interaction, cog: Choice[str]) -> None:
        await self.bot.load_extension(f'cogs.{cog.value}')
        await interaction.response.send_message(f'Successfully loaded ``{cog.name}``', ephemeral = True)

    
    @app_commands.command(name = 'unload', description = 'Unloads a cog')
    @app_commands.describe(cog = 'The cog to unload')
    @app_commands.choices(cog = cog_choices)
    @app_commands.check(is_owner)
    async def unload(self, interaction: discord.Interaction, cog: Choice[str]) -> None:
        await self.bot.unload_extension(f'cogs.{cog.value}')
        await interaction.response.send_message(f'Successfully unloaded ``{cog.name}``', ephemeral = True)


    @app_commands.command(name = 'reload', description = 'Reloads a cog')
    @app_commands.describe(cog = 'The cog to reload')
    @app_commands.choices(cog = cog_choices)
    @app_commands.check(is_owner)
    async def reload(self, interaction: discord.Interaction, cog: Choice[str]) -> None:
        await self.bot.reload_extension(f'cogs.{cog.value}')
        await interaction.response.send_message(f'Successfully reloaded ``{cog.name}``', ephemeral = True)

    
    @app_commands.command(name = 'sync', description = 'Syncs application commands')
    @app_commands.check(is_owner)
    async def sync(self, interaction: discord.Interaction) -> None:
        synced = await self.bot.tree.sync()
        await interaction.response.send_message(f'Successfully synced ``{len(synced)}`` application command(s)', ephemeral = True)

    
    @app_commands.command(name = 'status', description = 'Changes the bot\'s status')
    @app_commands.rename(online_status = 'status', activity_type = 'activity', activity_name = 'name')
    @app_commands.choices(
        online_status = [
            Choice(name = 'Online', value = 'online'),
            Choice(name = 'Idle', value = 'idle'),
            Choice(name = 'DND', value = 'dnd'),
            Choice(name = 'Invisible', value = 'invisible')
        ],
        activity_type = [
            Choice(name = 'None', value = -1),
            Choice(name = 'Playing', value = 0),
            Choice(name = 'Listening', value = 2),
            Choice(name = 'Watching', value = 3)
        ]
    )
    @app_commands.check(is_owner)
    async def status(self, interaction: discord.Interaction, online_status: Optional[Choice[str]], activity_type: Optional[Choice[int]], activity_name: Optional[str]) -> None:
        
        if online_status:
            self.bot.current_status['online_status'] = online_status.value

        if activity_type:
            self.bot.current_status['activity_type'] = activity_type.value

        if activity_name:
            self.bot.current_status['activity_name'] = activity_name
        
        tmp = self.bot.current_status
        await self.bot.change_presence(
            status = tmp['online_status'],
            activity = discord.Activity(type = tmp['activity_type'], name = tmp['activity_name'])
        )
        
        await interaction.response.send_message('Updated status!', ephemeral = True)

    
    # global error handlers
    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        
        if isinstance(error, commands.errors.NotOwner):
            await ctx.reply(f'Insufficient permissions to run command: ``{ctx.command.name}``')

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f'Missing required argument: ``{error.param.name}``')


    async def cog_app_command_error(self, interaction: discord.Interaction, error: Exception) -> None:

        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message(f'Insufficient permissions to run command: ``{interaction.command.name}``', ephemeral = True)


# setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))