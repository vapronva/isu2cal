from datetime import datetime

from ics import Calendar, Event, Organizer

from authenticate.id_itmo_ru import ITMOAuthenticator
from schedule.models import Lesson, Schedule


def main() -> None:
    authenticator = ITMOAuthenticator(
        client_id="profile",
        client_secret=None,
    )
    # if authenticator.is_expired():
    authenticator.refresh()
    schedule_response = authenticator.request(
        method="GET",
        url="https://api.schedule.itmo.su/api/v3/schedule/personal",
        language="ru",
        params={
            "date_start": "2023-09-06",
            "date_end": "2023-09-07",
        },
    ).json()
    for day in schedule_response["data"]:
        for lesson in day["lessons"]:
            lesson["date"] = day["date"]
    schedule = Schedule(**schedule_response)
    calendar = Calendar()
    lessons: list[Lesson] = []
    for day in schedule.data:
        for lesson in day.lessons:
            lessons.append(lesson)
    for lesson in lessons:
        calendar.events.add(
            Event(
                name=f"{lesson.subject} ({lesson.work_type.value.__str__().lower()})",
                begin=lesson.time_start,
                end=lesson.time_end,
                uid=lesson.pair_id.__str__(),
                description=lesson.note,
                location=f"Ауд. {lesson.room}; {lesson.building}",
                organizer=Organizer(
                    email=f"{lesson.teacher_id}",
                    common_name=f"{lesson.teacher_name or 'Unknown'}",
                ),
                categories=[lesson.group.strip()],
                status="CONFIRMED",
                url=lesson.zoom_url,
                last_modified=datetime.now(tz=lesson.time_start.tzinfo),
            ),
        )
    with open("schedule.ics", "w") as f:
        f.writelines(calendar.serialize_iter())


if __name__ == "__main__":
    main()
