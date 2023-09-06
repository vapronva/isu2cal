from datetime import datetime

from authenticate.id_itmo_ru import ITMOAuthenticator
from custom_i18n.langs import Languages
from ics_calendar.cal import create_calendar
from schedule.models import Lesson, Schedule


def main(
    start_date: datetime | str,
    end_date: datetime | str,
    language: Languages = Languages.ENGLISH,
) -> str:
    authenticator = ITMOAuthenticator(
        client_id="profile",
        client_secret=None,
    )
    if not authenticator.token_exists_and_is_valid():
        msg = "Token does not exist or is invalid"
        raise RuntimeError(msg)
    print(authenticator)
    schedule_response = authenticator.request(
        method="GET",
        url="https://api.schedule.itmo.su/api/v3/schedule/personal",
        language=language.value.__str__().lower(),
        params={
            "date_start": start_date.strftime("%Y-%m-%d")
            if isinstance(start_date, datetime)
            else start_date,
            "date_end": end_date.strftime("%Y-%m-%d")
            if isinstance(end_date, datetime)
            else end_date,
        },
    )
    print(schedule_response)
    schedule_response_json = schedule_response.json()
    for day in schedule_response_json["data"]:
        for lesson in day["lessons"]:
            lesson["date"] = day["date"]
    schedule = Schedule(**schedule_response_json)
    lessons: list[Lesson] = []
    for day in schedule.data:
        for lesson in day.lessons:
            lessons.append(lesson)
    calendar = create_calendar(language=language, lessons=lessons)
    return calendar.serialize()


if __name__ == "__main__":
    main("2023-09-07", "2023-09-10")
