from datetime import datetime, timedelta

from peewee import *

db = SqliteDatabase("strolly.db")


class BaseModel(Model):
    class Meta:
        database = db


class TwitchChannel(BaseModel):
    user_id = IntegerField(primary_key=True)
    display_name = CharField()
    emoji = CharField()


class Schedule(BaseModel):
    calendar_year = IntegerField()
    calendar_week = IntegerField()
    message_id = IntegerField(null=True)


class ScheduleSegment(BaseModel):
    id = CharField(primary_key=True)
    start_time = DateTimeField()
    end_time = DateTimeField(null=True)
    title = CharField()
    channel = ForeignKeyField(TwitchChannel, backref="schedule_segments")
    schedule = ForeignKeyField(Schedule, backref="schedule_segments")

    def timeframe(self):
        tf = f"<t:{int(datetime.fromisoformat(self.start_time).timestamp())}:t> - "
        end_time = datetime.fromisoformat(self.end_time) if self.end_time else datetime.fromisoformat(
            self.start_time) + timedelta(hours=4)
        tf += f"<t:{int(end_time.timestamp())}:t>"
        return tf


db.create_tables([TwitchChannel, Schedule, ScheduleSegment], safe=True)
