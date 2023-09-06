from enum import StrEnum, auto

from custom_i18n.langs import Languages
from schedule.models import Buildings, LessonFormats, LessonTypes


class NotesOfNotes(StrEnum):
    LESSON_NOTE = auto()
    FLOW_ID = auto()
    ZOOM_ID = auto()
    ZOOM_PASSWORD = auto()
    PAIR_ID = auto()
    GROUP_NAME = auto()


LESSON_TYPES_TR: dict[Languages, dict[LessonTypes, tuple[str, str]]] = {
    Languages.ENGLISH: {
        LessonTypes.LECTURE: ("lecture", "lecture"),
        LessonTypes.LABORATORY: ("laboratory class", "lab class"),
        LessonTypes.PRACTICAL: ("practical class", "practice"),
        LessonTypes.SPORT: ("sport", "sport"),
    },
    Languages.RUSSIAN: {
        LessonTypes.LECTURE: ("лекция", "лекция"),
        LessonTypes.LABORATORY: ("лабораторное занятие", "лабораторная"),
        LessonTypes.PRACTICAL: ("практическое занятие", "практика"),
        LessonTypes.SPORT: ("занятие спортом", "спорт"),
    },
}  # type: ignore

LESSON_FORMATS_TR: dict[Languages, dict[LessonFormats, tuple[str, str]]] = {
    Languages.ENGLISH: {
        LessonFormats.FACE_TO_FACE: ("face-to-face", "face-to-face"),
        LessonFormats.MIXED: ("face-to-face + distant", "mixed"),
        LessonFormats.DISTANCE: ("distance", "distant"),
    },
    Languages.RUSSIAN: {
        LessonFormats.FACE_TO_FACE: ("очный", "очно"),
        LessonFormats.MIXED: ("очно-дистанционный", "очно-дистант"),
        LessonFormats.DISTANCE: ("дистанционный", "дистант"),
    },
}  # type: ignore

BUILDINGS_TR: dict[Languages, dict[Buildings, tuple[str, str]]] = {
    Languages.ENGLISH: {
        Buildings.BIRZHEVAYA_14_A: ("Birzhevaya liniya, d. 14, lit. A", "Birzhevaya"),
        Buildings.GASTELLO_12_A: ("ul. Gastello, d. 12, lit. A", "Gastello"),
        Buildings.KRONV_49_A: ("Kronverksky pr., d. 49, lit. A", "Kronverksky"),
        Buildings.LOMO_9_A: ("ul. Lomonosova, d. 9, lit. A", "Lomonosova"),
        Buildings.LOMO_9_B: ("ul. Lomonosova, d. 9, lit. B", "Lomonosova"),
        Buildings.LOMO_9_E: ("ul. Lomonosova, d. 9, lit. E", "Lomonosova"),
        Buildings.LOMO_9_M: ("ul. Lomonosova, d. 9, lit. M", "Lomonosova"),
        Buildings.ALEXANDER_PARK_4: ("Aleksandrovsky park, 4", "Aleksandrovsky park"),
        Buildings.UNKNOWN: ("", ""),
    },
    Languages.RUSSIAN: {
        Buildings.BIRZHEVAYA_14_A: ("Биржевая линия, д. 14, лит. A", "Биржевая"),
        Buildings.GASTELLO_12_A: ("ул. Гастелло, д. 12, лит. A", "Гастелло"),
        Buildings.KRONV_49_A: ("Кронверкский пр., д. 49, лит. A", "Кронверкский"),
        Buildings.LOMO_9_A: ("ул. Ломоносова, д. 9, лит. A", "Ломоносова"),
        Buildings.LOMO_9_B: ("ул. Ломоносова, д. 9, лит. Б", "Ломоносова"),
        Buildings.LOMO_9_E: ("ул. Ломоносова, д. 9, лит. E", "Ломоносова"),
        Buildings.LOMO_9_M: ("ул. Ломоносова, д. 9, лит. M", "Ломоносова"),
        Buildings.ALEXANDER_PARK_4: ("Александровский парк, 4", "Александровский парк"),
        Buildings.UNKNOWN: ("", ""),
    },
}  # type: ignore

AUDITORIUMS_TR: dict[Languages, dict[int, tuple[str, str]]] = {
    Languages.ENGLISH: {
        0: ("auditorium", "aud."),
        1: ("room", "room"),
    },
    Languages.RUSSIAN: {
        0: ("аудитория", "ауд."),
        1: ("кабинет", "каб."),
    },
}

NOTES_TR: dict[Languages, dict[NotesOfNotes, str]] = {
    Languages.ENGLISH: {
        NotesOfNotes.LESSON_NOTE: "lesson note",
        NotesOfNotes.FLOW_ID: "flow ID",
        NotesOfNotes.ZOOM_ID: "zoom ID",
        NotesOfNotes.ZOOM_PASSWORD: "zoom password",
        NotesOfNotes.PAIR_ID: "pair ID",
        NotesOfNotes.GROUP_NAME: "group name",
    },
    Languages.RUSSIAN: {
        NotesOfNotes.LESSON_NOTE: "заметка к занятию",
        NotesOfNotes.FLOW_ID: "ID потока",
        NotesOfNotes.ZOOM_ID: "конференция в Zoom",
        NotesOfNotes.ZOOM_PASSWORD: "пароль в Zoom",
        NotesOfNotes.PAIR_ID: "ID пары",
        NotesOfNotes.GROUP_NAME: "название группы",
    },
}
