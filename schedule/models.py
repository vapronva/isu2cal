from datetime import datetime
from enum import StrEnum

from aenum import MultiValueEnum
from pydantic import BaseModel


class LessonFormats(StrEnum):
    FULL_TIME = "Очный"
    DISTANCE = "Дистанционный "
    MIXED = "Очно - дистанционный "


class LessonTypes(MultiValueEnum):
    LABORATORY = "Лабораторные занятия", "Laboratory classes"
    LECTURE = "Лекции", "Lectures"
    SPORT = "Занятия спортом", "Sport"
    PRACTICAL = "Практические занятия", "Practical classes"


class Lesson(BaseModel):
    date: str
    pair_id: int
    subject: str
    subject_id: int
    note: str | None
    type: str | LessonTypes | None
    time_start: datetime
    time_end: datetime
    teacher_id: int | None
    teacher_name: str | None
    room: str | None
    building: str | None
    format: LessonFormats
    work_type: LessonTypes
    work_type_id: int
    group: str
    flow_type_id: int
    flow_id: int
    zoom_url: str | None
    zoom_password: str | None
    zoom_info: str | None
    bld_id: int | None
    format_id: int
    main_bld_id: int | None

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
