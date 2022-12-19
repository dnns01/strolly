import base64
import json
import os
from datetime import datetime, timedelta

import discord
from discord import app_commands, Interaction
from discord.ext import commands, tasks
from twitchio import Client

from models import ScheduleSegment, TwitchChannel, Schedule


def get_calendar_week():
    now = datetime.now()
    calendar = now.isocalendar()

    if calendar.weekday < 7 or now.hour < 12:
        start_day = now - timedelta(days=calendar.weekday - 1)
        return calendar.week, datetime(year=start_day.year, month=start_day.month, day=start_day.day)

    start_day = now + timedelta(days=1)
    return start_day.isocalendar().week, datetime(year=start_day.year, month=start_day.month, day=start_day.day)


def get_weekday(curr_day):
    weekdays = ["", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    return weekdays[curr_day.isocalendar().weekday]


def remove_cancelled_streams(user, segments):
    segments_dict = {segment.id: segment for segment in segments}

    for schedule_segment in ScheduleSegment.select().where(ScheduleSegment.channel == user.id).where(
            ScheduleSegment.start_time > datetime.now()):
        if schedule_segment.id not in segments_dict:
            schedule_segment.delete_instance()


@app_commands.guild_only
@app_commands.default_permissions(manage_server=True)
class TwitchSchedule(commands.GroupCog, name="schedule"):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_client = Client.from_client_credentials(client_id=os.getenv("TWITCH_CLIENT_ID"),
                                                            client_secret=os.getenv("TWITCH_CLIENT_SECRET"))
        self.update_task.start()

    @app_commands.command(name="add", description="Add Twitch channel to schedule")
    @app_commands.describe(twitch_channel="Twitch channel to add",
                           emoji="Emoji to be used for this channels entries in schedule",
                           update_schedule="Define whether schedule should be updated or not.")
    async def cmd_add(self, interaction: Interaction, twitch_channel: str, emoji: str, update_schedule: bool = False):
        await interaction.response.defer(ephemeral=True)
        user = await self.twitch_client.fetch_users(names=[twitch_channel])
        if len(user) != 1:
            await interaction.edit_original_response(
                content="Twitch Kanal nicht gefunden. Bitte überprüfe, ob du den Kanal richtig geschrieben hast.")
            return

        if TwitchChannel.get_or_none(TwitchChannel.user_id == user[0].id):
            await interaction.edit_original_response(
                content="Der angegebene Kanal ist schon Teil des Kalenders.")
            return

        TwitchChannel.create(user_id=user[0].id, emoji=emoji, display_name=user[0].display_name)
        await interaction.edit_original_response(
            content=f"Twitch Kanal {twitch_channel} erfolgreich hinzugefügt.")
        if update_schedule:
            await self.update_schedule()

    @app_commands.command(name="remove", description="Remove Twitch Channel from Schedule")
    @app_commands.describe(twitch_channel="Twitch Channel to remove",
                           update_schedule="Define whether Schedule should be updated or not.")
    async def cmd_remove(self, interaction: Interaction, twitch_channel: str, update_schedule: bool = False):
        await interaction.response.defer(ephemeral=True)
        user = await self.twitch_client.fetch_users(names=[twitch_channel])
        if len(user) != 1:
            await interaction.edit_original_response(
                content="Twitch Kanal nicht gefunden. Bitte überprüfe, ob du den Kanal richtig geschrieben hast.")
            return

        if channel := TwitchChannel.get_or_none(TwitchChannel.user_id == user[0].id):
            channel.delete_instance(recursive=True)
            await interaction.edit_original_response(
                content=f"Twitch Kanal {twitch_channel} erfolgreich entfernt.")
            if update_schedule:
                await self.update_schedule()
            return

        await interaction.edit_original_response(
            content=f"Twitch Kanal ist kein Teil des Kalenders.")

    @app_commands.command(name="update", description="Force to update the schedule")
    async def cmd_update(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.update_schedule()
        await interaction.edit_original_response(content="Update abgeschlossen.")

    @tasks.loop(hours=1)
    async def update_task(self):
        await self.update_schedule()

    async def update_schedule(self):
        await self.update_database()
        calendar_week, start_day = get_calendar_week()
        end_day = start_day + timedelta(days=6)

        schedule_channel = await self.bot.fetch_channel(int(os.getenv("SCHEDULE_CHANNEL")))

        week_schedule = Schedule.get_or_none(calendar_week=calendar_week, calendar_year=start_day.year)
        embed = discord.Embed(title=f"Contentvorhersage für die {calendar_week}. Kalenderwoche",
                              description=f"Strolchige Streams in der Woche vom {start_day.strftime('%d.%m.%Y')} "
                                          f"bis {end_day.strftime('%d.%m.%Y')}")
        embed.set_thumbnail(url="https://strolchibot.dnns01.dev/static/images/logo.png")

        curr_day = start_day
        while curr_day <= end_day:
            name = f"{get_weekday(curr_day)} {curr_day.strftime('%d.%m.%Y')}"
            value = ""
            for segment in ScheduleSegment.select() \
                    .where(ScheduleSegment.start_time.between(curr_day, (curr_day + timedelta(days=1)))) \
                    .order_by(ScheduleSegment.start_time):
                value += f"{segment.channel.emoji} {segment.timeframe()}\n{segment.title}\n\n"

            if len(value) > 0:
                embed.add_field(name=name, value=value, inline=False)
            curr_day += timedelta(days=1)

        if week_schedule.message_id:
            try:
                message = await schedule_channel.fetch_message(week_schedule.message_id)
                await message.edit(embed=embed)
                return
            except:
                pass

        message = await schedule_channel.send("", embed=embed)
        week_schedule.update(message_id=message.id).where(Schedule.id == week_schedule.id).execute()

    async def update_database(self):
        twitch_channels = [twitch_channel.user_id for twitch_channel in TwitchChannel.select()]
        for user in await self.twitch_client.fetch_users(ids=twitch_channels):
            schedule = await user.fetch_schedule()
            for segment in schedule.segments:
                segment_id = json.loads(base64.b64decode(segment.id))
                calendar_year = segment_id["isoYear"]
                calendar_week = segment_id["isoWeek"]
                week_schedule = Schedule.get_or_create(calendar_week=calendar_week, calendar_year=calendar_year)
                if segment.start_time < datetime.now().astimezone():
                    continue
                if schedule_segment := ScheduleSegment.get_or_none(
                        ScheduleSegment.id == segment.id):
                    schedule_segment.update(start_time=segment.start_time, end_time=segment.end_time,
                                            title=segment.title, schedule=week_schedule[0].id) \
                        .where(ScheduleSegment.id == segment.id).execute()
                else:
                    ScheduleSegment.create(id=segment.id, start_time=segment.start_time, end_time=segment.end_time,
                                           title=segment.title, channel=user.id, schedule=week_schedule[0].id)

            remove_cancelled_streams(user, schedule.segments)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TwitchSchedule(bot))
