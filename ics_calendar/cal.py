from datetime import date, datetime, timedelta
from datetime import time as d_time
from pathlib import Path

import ics

from custom_i18n.langs import Languages
from custom_i18n.schd import AUDITORIUMS_TR, BUILDINGS_TR, LESSON_TYPES_TR
from schedule.models import Lesson


def get_week_range_datetimes() -> tuple[datetime, datetime]:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return datetime.combine(start_of_week, d_time.min), datetime.combine(
        end_of_week,
        d_time.max,
    )


class Calendar:
    def __init__(self, language: Languages) -> None:
        self._calendar = ics.Calendar()
        self.language = language

    def add_event(self, lesson: Lesson) -> None:
        self._calendar.events.add(
            ics.Event(
                name=f"{lesson.subject} ({LESSON_TYPES_TR[self.language][lesson.work_type_id][1]})".title() if self.language is Languages.ENGLISH else f"{lesson.subject} ({LESSON_TYPES_TR[self.language][lesson.work_type_id][1]})",
                begin=lesson.time_start,
                end=lesson.time_end,
                uid=lesson.pair_id.__str__(),
                description=Calendar.generate_description(lesson),
                location=f"{AUDITORIUMS_TR[self.language][0][1].title()} {lesson.room}; {BUILDINGS_TR[self.language][lesson.bld_id][0] if lesson.bld_id else ''}",
                organizer=ics.Organizer(
                    email=f"{lesson.teacher_id}",
                    common_name=f"{lesson.teacher_name or 'Unknown'}",
                ),
                categories=[lesson.group.strip()],
                status="CONFIRMED",
                url=lesson.zoom_url,
                last_modified=datetime.now(tz=lesson.time_start.tzinfo),
            ),
        )

    def serialize(self) -> str:
        return self._calendar.serialize()

    def write_to_file(self, filename: Path):
        with filename.open(mode="w") as f:
            f.writelines(self.serialize())

    @staticmethod
    def generate_description(lesson: Lesson) -> str:
        return ""


def create_calendar(language: Languages, lessons: list[Lesson]) -> Calendar:
    calendar = Calendar(language)
    for lesson in lessons:
        calendar.add_event(lesson)
    return calendar
