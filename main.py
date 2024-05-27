# discord.py imports
import discord
from discord.ext import commands

# misc imports
import os
import sys
import asyncio

# initialize env
from dotenv import load_dotenv
load_dotenv('.env')


# variables
TOKEN: str = os.getenv('token')
OWNER: int = int(os.getenv('owner'))
PREFIX: str = os.getenv('prefix')


# bot class
class Sora(commands.Bot):

    def __init__(self):

        # initialize bot
        super().__init__(
            owner_id = OWNER,
            command_prefix = PREFIX,
            intents = discord.Intents.all(),
            help_command = None,
            status = discord.Status.online
        )


    async def setup_hook(self) -> None:

        self.current_status = {
            'online_status': self.status,
            'activity_type': None,
            'activity_name': None
        }

        # load cogs
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')


    # event listeners
    async def on_ready(self) -> None:
        print(f'Logged in as {self.user}')


# main
async def main():

    discord.utils.setup_logging()

    async with Sora() as bot:
        await bot.start(TOKEN)

try:
    asyncio.run(main())

except KeyboardInterrupt:
    sys.exit()