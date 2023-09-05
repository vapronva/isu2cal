from datetime import datetime

from aenum import MultiValueEnum
from pydantic import BaseModel


class LessonFormats(MultiValueEnum):
    FACE_TO_FACE: tuple[str | int, ...] = "Очный", 1
    MIXED: tuple[str | int, ...] = "Очно - дистанционный ", 2
    DISTANCE: tuple[str | int, ...] = "Дистанционный ", 3


class LessonTypes(MultiValueEnum):
    LECTURE: tuple[str | int, ...] = "Лекции", "Lectures", 1
    LABORATORY: tuple[str | int, ...] = "Лабораторные занятия", "Laboratory classes", 2
    PRACTICAL: tuple[str | int, ...] = "Практические занятия", "Practical classes", 3
    SPORT: tuple[str | int, ...] = "Занятия спортом", "Sport", 11


class Buildings(MultiValueEnum):
    BIRZHEVAYA_14_A = 1, "Биржевая линия, д.14, лит.A", "Birzhevaya liniya, d.14, lit.A"
    GASTELLO_12_A = 6, "ул.Гастелло, д.12, лит.A", "ul.Gastello, d.12, lit.A"
    KRONV_49_A = 13, "Кронверкский пр., д.49, лит.A", "Kronverksky pr., d.49, lit.A"
    LOMO_9_A = 23, "ул.Ломоносова, д.9, лит. A", "ul.Lomonosova, d.9, lit. A"
    LOMO_9_B = 33, "ул.Ломоносова, д.9, лит. Б", "ul.Lomonosova, d.9, lit. B"
    LOMO_9_E = 35, "ул.Ломоносова, д.9, лит. E", "ul.Lomonosova, d.9, lit. E"
    LOMO_9_M = 37, "ул.Ломоносова, д.9, лит. M", "ul.Lomonosova, d.9, lit. M"
    ALEXANDER_PARK_4 = 343, "Александровский парк, 4", "Aleksandrovsky park, 4"
    UNKNOWN = None


class Lesson(BaseModel):
    date: str
    pair_id: int | str
    subject: str | None
    subject_id: int
    note: str | None
    time_start: datetime
    time_end: datetime
    teacher_name: str | None
    teacher_id: int | None
    room: str | None
    building: Buildings | None
    bld_id: Buildings | None
    main_bld_id: int | None
    format: LessonFormats
    format_id: LessonFormats
    type: str | LessonTypes | None
    work_type: LessonTypes
    work_type_id: LessonTypes
    group: str
    flow_type_id: int
    flow_id: int
    zoom_url: str | None
    zoom_password: str | None
    zoom_info: str | None

    def __init__(self, **data) -> None:
        data["time_start"] = datetime.strptime(
            f"{data['date']}T{data['time_start']}+0300",
            "%Y-%m-%dT%H:%M%z",
        )
        data["time_end"] = datetime.strptime(
            f"{data['date']}T{data['time_end']}+0300",
            "%Y-%m-%dT%H:%M%z",
        )
        super().__init__(**data)


class Day(BaseModel):
    day_number: int
    week_number: int
    date: str
    note: str | None
    type: str | None
    lessons: list[Lesson]
    intersections: list[list[int]] | None


class Schedule(BaseModel):
    code: int
    data: list[Day]
    message: str | None
