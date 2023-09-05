from datetime import date, datetime, timedelta
from datetime import time as d_time
from pathlib import Path

import ics

from authenticate.id_itmo_ru import ITMOAuthenticator
from schedule.models import Lesson, Schedule


def get_week_range_datetimes() -> tuple[datetime, datetime]:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return datetime.combine(start_of_week, d_time.min), datetime.combine(
        end_of_week,
        d_time.max,
    )


class Calendar:
    def __init__(self, language) -> None:
        self._calendar = ics.Calendar()
        self.language = language

    def add_event(self, lesson: Lesson) -> None:
        self._calendar.events.add(
            ics.Event(
                name=f"{lesson.subject} ({lesson.work_type.value.__str__().lower()})",
                begin=lesson.time_start,
                end=lesson.time_end,
                uid=lesson.pair_id.__str__(),
                description=lesson.note,
                location=f"Ауд. {lesson.room}; {lesson.building}",
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


def create_calendar(language: str, lessons: list[Lesson]) -> Calendar:
    calendar = Calendar(language)
    for lesson in lessons:
        calendar.add_event(lesson)
    return calendar


def main(start_date: datetime, end_date: datetime) -> None:
    authenticator = ITMOAuthenticator(
        client_id="profile",
        client_secret=None,
    )
    authenticator.refresh()
    schedule_response = authenticator.request(
        method="GET",
        url="https://api.schedule.itmo.su/api/v3/schedule/personal",
        language="ru",
        params={
            "date_start": start_date.strftime("%Y-%m-%d"),
            "date_end": end_date.strftime("%Y-%m-%d"),
        },
    ).json()
    for day in schedule_response["data"]:
        for lesson in day["lessons"]:
            lesson["date"] = day["date"]
    schedule = Schedule(**schedule_response)
    lessons: list[Lesson] = []
    for day in schedule.data:
        for lesson in day.lessons:
            lessons.append(lesson)
    calendar = create_calendar(language="ru", lessons=lessons)
    calendar.write_to_file(Path("schedule.ics"))


if __name__ == "__main__":
    main(*get_week_range_datetimes())
