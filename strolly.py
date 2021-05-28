import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from armin import Armin
from leaderboard import Leaderboard
from poll_cog import PollCog
from roll_cog import RollCog
from schedule import Schedule

# .env file is necessary in the same directory, that contains several strings.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = os.getenv('DISCORD_ACTIVITY')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', help_command=None, activity=discord.Game(ACTIVITY), intents=intents)
bot.add_cog(PollCog(bot))
bot.add_cog(RollCog(bot))
bot.add_cog(Leaderboard(bot))
bot.add_cog(Armin(bot))
bot.add_cog(Schedule(bot))


@bot.event
async def on_ready():
    print("Client started!")


bot.run(TOKEN)
