from pydantic import BaseModel
from datetime import date


class GroupSchema(BaseModel):
    group_num: int | None = None
    faculty: str | None = None
    qualification: str | None = None
    creation: int | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class StudentSchema(BaseModel):
    fio: str | None = None
    group_id: int | None = None
    book_num: int | None = None
    birth: date | None = None
    enrollment: int | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ThemeSchema(BaseModel):
    name: str | None = None
    complexity: int | None = None
    first_time: int | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class SourceSchema(BaseModel):
    name: str | None = None
    type: str | None = None
    authors: str | None = None
    creation: int | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ProjectSchema(BaseModel):
    theme_id: int | None = None
    author_id: int | None = None
    mark: int | None = None
    passed: date| None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class SourceProjectSchema(BaseModel):
    source_id: int | None = None
    project_id: int | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

