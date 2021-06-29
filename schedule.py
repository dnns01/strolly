import json
import os
from datetime import datetime

import discord
from aiohttp import ClientSession
from discord.ext import commands, tasks


async def get_schedule():
    async with ClientSession() as session:
        auth = "kimne78kx3ncx6brgo4mv6wki5h1ko"
        headers = {"client-id": f"{auth}", "Content-Type": "application/json"}

        async with session.post("https://gql.twitch.tv/gql",
                                headers=headers,
                                json={
                                    "query": "query {\r\n channel(name: \"indiestrolche\") {\r\n schedule {\r\n segments(includeFutureSegments: true) {\r\n id\r\n startAt\r\n title\r\n categories {\r\n displayName\r\n boxArtURL\r\n }\r\n }\r\n }\r\n }\r\n}"}) as r:
            if r.status == 200:
                return {segment["id"]: segment for segment in
                        (await r.json())["data"]["channel"]["schedule"]["segments"]}
    return None


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_schedule.start()
        self.schedule_file = "schedule.json"
        self.schedule = self.load()

    def load(self):
        schedule_file = open(self.schedule_file, mode="r")
        return json.load(schedule_file)

    def save(self):
        schedule_file = open(self.schedule_file, mode="w")
        json.dump(self.schedule, schedule_file)

    @tasks.loop(hours=1)
    async def update_schedule(self):
        new_schedule = await get_schedule()

        for id, segment in new_schedule.items():
            if id in self.schedule.keys():
                old_segment = self.schedule.get(id)
                if old_segment["startAt"] != segment["startAt"]:
                    self.schedule[id] = segment
                    await self.announce_segment(segment, new=False)
            else:
                self.schedule[id] = segment
                await self.announce_segment(segment)
        self.save()

    async def announce_segment(self, segment, new=True):
        channel = await self.bot.fetch_channel(int(os.getenv("DURCHSAGEN_CHANNEL")))
        start_at = datetime.fromisoformat(f"{segment['startAt'][:-1]}+00:00").astimezone().strftime("%d.%m.%Y %H:%M")
        title = "<:ja:836282702248411217> <:aa:836282738709233675> <:aa:836282738709233675> <:aa:836282738709233675> <:aa:836282738709233675>" if new else "Achtung Leute aufgepasst!!!"
        description = "Wie geil ist es? Ein neuer Stream ist in den Kalender geglitten\n" if new else "Es gibt eine kleine Änderung im Programmablauf!\n"
        game = "Lass dich einfach überraschen!"
        url = "https://static-cdn.jtvnw.net/ttv-static/404_boxart-144x192.jpg"
        if categories := segment.get("categories"):
            game = categories[0]['displayName']
            url = categories[0]['boxArtURL'].replace('-{width}x{height}', '').replace("/./", "/")
        embed = discord.Embed(title=title, description=description)
        embed.set_thumbnail(url=url)
        embed.add_field(name=segment["title"], value=game)
        embed.add_field(name="Wann?", value=start_at)
        await channel.send(embed=embed)
