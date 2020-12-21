import random

from discord.ext import commands


class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def cmd_roll(self, ctx, dice="w6", qty=1):
        """ Roll a/multiple dice """

        eyes = int(dice[1:])
        answer = f"Es wurden {qty} {dice.upper()} geworfen, mit folgenden Ergebnissen:\n"
        for i in range(qty):
            answer += f"{i + 1}. Wurf: {random.randrange(1, eyes + 1)}\n"

        await ctx.send(answer)
