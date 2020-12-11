import os
import random
from time import time, sleep

from discord.ext import commands


class BatiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bati_id = int(os.getenv("BATI_ID"))
        self.last_bati = 0
        self.bati_probability = float(os.getenv("BATI_PROBABILITY"))
        self.bati_delay = int(os.getenv("BATI_DELAY"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bati_id:
            if random.random() < self.bati_probability and time() >= self.last_bati + (self.bati_delay * 3600):
                sleep(random.random() * 2)
                await message.channel.send("bati")
                self.last_bati = time()
            print(message.content)
