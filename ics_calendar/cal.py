from datetime import date, datetime, timedelta
from datetime import time as d_time
from pathlib import Path

import ics

from custom_i18n.langs import Languages
from custom_i18n.schd import (
    AUDITORIUMS_TR,
    BUILDINGS_TR,
    LESSON_TYPES_TR,
    NOTES_TR,
    NotesOfNotes,
)
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
                name=camelcase_title(
                    f"{lesson.subject} ({LESSON_TYPES_TR[self.language][lesson.work_type_id][1]})",
                )
                if self.language is Languages.ENGLISH
                else f"{lesson.subject} ({LESSON_TYPES_TR[self.language][lesson.work_type_id][1]})",
                begin=lesson.time_start,
                end=lesson.time_end,
                uid=lesson.pair_id.__str__(),
                description=self.generate_description(lesson),
                location=f"{AUDITORIUMS_TR[self.language][0][1].title()} {lesson.room}; {BUILDINGS_TR[self.language][lesson.bld_id][0] if lesson.bld_id else ''}"
                if lesson.room is not None or lesson.bld_id is not None
                else None,
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

    def generate_description(self, lesson: Lesson) -> str:
        output_string: str = ""
        output_string += self.add_note_to_output_string(
            lesson.note,
            NotesOfNotes.LESSON_NOTE,
        )
        output_string += self.add_note_to_output_string(
            lesson.flow_id.__str__(),
            NotesOfNotes.FLOW_ID,
        )
        output_string += self.add_note_to_output_string(
            lesson.zoom_url,
            NotesOfNotes.ZOOM_ID,
        )
        output_string += self.add_note_to_output_string(
            lesson.zoom_password,
            NotesOfNotes.ZOOM_PASSWORD,
        )
        output_string += self.add_note_to_output_string(
            lesson.group,
            NotesOfNotes.GROUP_NAME,
        )
        print(output_string)
        return output_string.strip()

    def add_note_to_output_string(
        self,
        note: str | None,
        note_type: NotesOfNotes,
    ) -> str:
        if note is not None:
            return f"{camelcase_title(NOTES_TR[self.language][note_type], self.language)}: {note}\n"
        return ""


def camelcase_title(title: str, language: Languages = Languages.ENGLISH) -> str:
    EXCEPTIONS: set[str] = {
        "of",
        "the",
        "and",
        "in",
        "to",
        "a",
        "an",
        "for",
        "on",
        "at",
        "from",
        "by",
        "with",
        "or",
        "as",
        "but",
        "into",
        "like",
        "through",
        "after",
        "over",
        "between",
        "out",
        "against",
        "during",
        "without",
        "before",
        "under",
        "around",
        "among",
        "about",
        "ITMO",
        "ID",
        "URL",
        "Zoom",
    }
    if language is Languages.ENGLISH:
        return " ".join(
            [
                word.title() if word not in EXCEPTIONS else word
                for word in title.split()
            ],
        )
    else:
        resulting_words = []
        for i, word in enumerate(title.split()):
            if i == 0:
                resulting_words.append(
                    word.capitalize() if word not in EXCEPTIONS else word,
                )
            else:
                resulting_words.append(word.lower() if word not in EXCEPTIONS else word)
        return " ".join(resulting_words)


def create_calendar(language: Languages, lessons: list[Lesson]) -> Calendar:
    calendar = Calendar(language)
    for lesson in lessons:
        calendar.add_event(lesson)
    return calendar
