from pydantic import BaseModel


class Lesson(BaseModel):
    pair_id: int
    subject: str
    subject_id: int
    note: str | None
    type: str | None
    time_start: str
    time_end: str
    teacher_id: int | None
    teacher_name: str | None
    room: str
    building: str
    format: str
    work_type: str
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


class Day(BaseModel):
    day_number: int
    week_number: int
    date: str
    note: str | None
    type: str | None
    lessons: list[Lesson]
    intersections: list[list[int]]


class Schedule(BaseModel):
    code: int
    data: list[Day]
    message: str | None
