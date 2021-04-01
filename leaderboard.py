import json

import discord
from discord.ext import commands


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.highscores = self.load()

    def load(self):
        """ Load highscores from json file """
        highscore_file = open("highscores.json", mode="r")
        return json.load(highscore_file)

    def save(self):
        """ Save highscores to json file """
        highscore_file = open("highscores.json", mode="w")
        json.dump(self.highscores, highscore_file)

    @commands.command(name="highscore")
    async def cmd_highscore(self, ctx, score: int):
        """ Add highscore for Dorfromantik leaderboard """

        if score > 50:
            if highscore := self.highscores.get(str(ctx.author.id)):
                self.highscores[str(ctx.author.id)] = max(highscore, score)
            else:
                self.highscores[str(ctx.author.id)] = score
            self.save()

            await ctx.send(
                f"Vielen Dank für deine Einreichung. Du bist damit auf Platz {self.get_place(ctx.author.id)} der Rangliste gelandet.")

    @commands.command(name="romantikboard", aliases=["dorfpranger"])
    async def cmd_romantikboard(self, ctx, all=None):

        embed = discord.Embed(title="Dorfromantik Leaderboard",
                              description="Offizielles inoffizielles Leaderborad des kultigen Karten-Lege-Spiels Dorfromantik der geilsten Powercommunity! Highscores, die HIER nicht eingetragen sind, zählen nicht!")
        embed.set_thumbnail(url="https://img.itch.zone/aW1nLzQ2ODEyMTUuanBn/original/SVutRj.jpg")

        places = scores = ""
        place = 0
        max = 0 if all == "all" else 10
        ready = False
        for key, value in sorted(self.highscores.items(), key=lambda item: item[1], reverse=True):
            try:
                place += 1

                if 0 < max < place:
                    if ready:
                        break
                    elif str(ctx.author.id) != key:
                        continue
                places += f"{place}: <@!{key}>\n"
                scores += f"{value:,}\n".replace(",", ".")

                if str(ctx.author.id) == key:
                    ready = True
            except:
                pass

        embed.add_field(name=f"Romantiker", value=places)
        embed.add_field(name=f"Punkte", value=scores)
        await ctx.send("", embed=embed)

    def get_place(self, id):
        place = 0
        for key, value in sorted(self.highscores.items(), key=lambda item: item[1], reverse=True):
            place += 1
            if key == str(id):
                return place
