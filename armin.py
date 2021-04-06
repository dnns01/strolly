import random

from discord.ext import commands


class Armin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = ["ein-", "zwei-", "drei-", "vier-", "fünf", "sechs-"]
        self.b = ["tägige/n", "wöchige/n", "monatige/n", "fache/n", "malige/n", "hebige/n"]
        self.c = ["harte/n", "softe/n", "optionale/n", "intranspatente/n", "alternativlose/n", "unumkehrbare/n"]
        self.d = ["Wellenbrecher-", "Brücken-", "Treppen-", "Wende-", "Impf-", "Ehren-"]
        self.e = ["Lockdown", "Stopp", "Maßnahme", "Kampagne", "Sprint", "Matrix"]
        self.f = ["zum Sommer", "auf Weiteres", "zur Bundestagswahl", "2030", "nach den Apiturprüfungen",
                  "in die Puppen"]
        self.g = ["sofortigen", "nachhaltigen", "allmählichen", "unausweichlichen", "wirtschaftsschonenden",
                  "willkürlichen"]
        self.h = ["Senkung", "Steigerung", "Beendigung", "Halbierung", "Vernichtung", "Beschönigung"]
        self.i = ["Infektionszahlen", "privaten Treffen", "Wirtschaftsleistung", "Wahlprognosen", "dritten Welle",
                  "Bundeskanzlerin"]

    @commands.command(name="arminsagt")
    async def cmd_arminsagt(self, ctx):
        await ctx.send(f"Was wir jetzt brauchen, ist ein/e {random.choice(self.a)}{random.choice(self.b)} "
                       f"{random.choice(self.c)} {random.choice(self.d)}{random.choice(self.e)} "
                       f"bis {random.choice(self.f)} zur {random.choice(self.g)} {random.choice(self.h)} "
                       f"der {random.choice(self.i)}.")
