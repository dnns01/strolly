import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bati_cog import BatiCog
from poll_cog import PollCog
from roll_cog import RollCog

# .env file is necessary in the same directory, that contains several strings.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ACTIVITY = os.getenv('DISCORD_ACTIVITY')
# HELP_FILE = os.getenv('DISCORD_HELP_FILE')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', help_command=None, activity=discord.Game(ACTIVITY), intents=intents)
bot.add_cog(PollCog(bot))
bot.add_cog(RollCog(bot))
bot.add_cog(BatiCog(bot))


# @bot.command(name="help")
# async def cmd_help(ctx):
#     """ Send help message as DM """
#
#     help_file = open(HELP_FILE, mode='r')
#     help_dict = json.load(help_file)
#     embed = discord.Embed.from_dict(help_dict)
#     await utils.send_dm(ctx.author, "", embed=embed)


@bot.event
async def on_ready():
    print("Client started!")
    # channel = await bot.fetch_channel(682590504948334684)
    # await channel.send("!poll \"Wie kluk bin ich?\" Sehr")


#

bot.run(TOKEN)
