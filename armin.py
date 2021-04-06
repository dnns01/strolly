import random
from datetime import datetime, timedelta

from discord.ext import commands


class Armin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = ["ein", "zwei", "drei", "vier", "fünf", "sechs"]
        self.b = ["tägige", "wöchige", "monatige", "fache", "malige", "hebige"]
        self.c = ["harte", "softe", "optionale", "intranspatente", "alternativlose", "unumkehrbare"]
        self.d = ["Wellenbrecher-", "Brücken-", "Treppen-", "Wende-", "Impf-", "Ehren-"]
        self.e = ["Lockdown", "Stopp", "Maßnahme", "Kampagne", "Sprint", "Matrix"]
        self.f = ["zum Sommer", "auf Weiteres", "zur Bundestagswahl", "2030", "nach den Abiturprüfungen",
                  "in die Puppen"]
        self.g = ["sofortigen", "nachhaltigen", "allmählichen", "unausweichlichen", "wirtschaftsschonenden",
                  "willkürlichen"]
        self.h = ["Senkung", "Steigerung", "Beendigung", "Halbierung", "Vernichtung", "Beschönigung"]
        self.i = ["Infektionszahlen", "privaten Treffen", "Wirtschaftsleistung", "Wahlprognosen", "dritten Welle",
                  "Bundeskanzlerin"]
        self.arminsagt_cooldown = datetime.now()

    @commands.command(name="arminsagt")
    async def cmd_arminsagt(self, ctx):
        if datetime.now() > self.arminsagt_cooldown:
            self.arminsagt_cooldown = datetime.now() + timedelta(minutes=1)
            rNum = random.randint(0, 5)
            n = "n" if rNum not in [2, 3, 5] else ""
            await ctx.send(f"Was wir jetzt brauchen, ist eine{n} {random.choice(self.a)}{random.choice(self.b)}{n} "
                           f"{random.choice(self.c)}{n} {random.choice(self.d)}{self.e[rNum]} "
                           f"bis {random.choice(self.f)} zur {random.choice(self.g)} {random.choice(self.h)} "
                           f"der {random.choice(self.i)}.")
        else:
            await ctx.send("Sorry, aber Armin denkt noch nach...")
