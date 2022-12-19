import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env file is necessary in the same directory, that contains several strings.
load_dotenv()


class Strolly(commands.Bot):
    def __init__(self, *args, initial_extensions: List[str], **kwargs):
        super(Strolly, self).__init__(*args, **kwargs)
        self.initial_extensions: List[str] = initial_extensions

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(f"extensions.{extension}")
        await self.tree.sync()


extensions = ["schedule"]
bot = Strolly(command_prefix="!", help_command=None, activity=discord.Game(os.getenv('DISCORD_ACTIVITY')),
              intents=discord.Intents.all(), initial_extensions=extensions)
bot.run(os.getenv('DISCORD_TOKEN'))
