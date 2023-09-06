from datetime import datetime

from aenum import MultiValueEnum
from pydantic import BaseModel


class LessonFormats(MultiValueEnum):
    FACE_TO_FACE: tuple[str | int, ...] = 1, "Очный"
    MIXED: tuple[str | int, ...] = 2, "Очно - дистанционный "
    DISTANCE: tuple[str | int, ...] = 3, "Дистанционный "


class LessonTypes(MultiValueEnum):
    LECTURE: tuple[str | int, ...] = 1, "Лекции", "Lectures"
    LABORATORY: tuple[str | int, ...] = 2, "Лабораторные занятия", "Laboratory classes"
    PRACTICAL: tuple[str | int, ...] = 3, "Практические занятия", "Practical classes"
    SPORT: tuple[str | int, ...] = 11, "Занятия спортом", "Sport"


class Buildings(MultiValueEnum):
    BIRZHEVAYA_14_A = 1, "Биржевая линия, д.14, лит.А", "Birzhevaya liniya, d.14, lit.A"
    GASTELLO_12_A = 6, "ул.Гастелло, д.12, лит.А", "ul.Gastello, d.12, lit.A"
    KRONV_49_A = 13, "Кронверкский пр., д.49, лит.А", "Kronverksky pr., d.49, lit.A"
    LOMO_9_A = 23, "ул.Ломоносова, д.9, лит. А", "ul.Lomonosova, d.9, lit. A"
    LOMO_9_B = 33, "ул.Ломоносова, д.9, лит. Б", "ul.Lomonosova, d.9, lit. B"
    LOMO_9_E = 35, "ул.Ломоносова, д.9, лит. Е", "ul.Lomonosova, d.9, lit. E"
    LOMO_9_M = 37, "ул.Ломоносова, д.9, лит. М", "ul.Lomonosova, d.9, lit. M"
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
