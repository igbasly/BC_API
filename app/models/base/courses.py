from typing import List
from pydantic import BaseModel


class ClassModule(BaseModel):
    day: int
    module: int
    type: str

    @classmethod
    def get_attributes(cls: BaseModel):
        base_attr = cls.__fields__
        attrs = {}
        for key in base_attr:
            type_ = base_attr[key]._type_display()
            if "List" in type_:
                attrs[key] = []  # pragma: no cover
            elif "Dict" in type_:
                attrs[key] = {}  # pragma: no cover
            else:
                attrs[key] = None
        return attrs


class Section(BaseModel):
    semester: str
    name: str
    course_code: str
    section: int
    section_id: int
    english_version: bool
    format: str
    category: str
    teacher_name: str
    campus: str
    value: int
    total_vacancies: int
    available_vacancies: int
    modules: List[ClassModule]

    @classmethod
    def get_attributes(cls: BaseModel):
        base_attr = cls.__fields__
        attrs = {}
        for key in base_attr:
            type_ = base_attr[key]._type_display()
            if "List" in type_:
                attrs[key] = []  # pragma: no cover
            elif "Dict" in type_:
                attrs[key] = {}  # pragma: no cover
            else:
                attrs[key] = None
        return attrs


class Course(BaseModel):
    semester: str
    name: str
    course_code: str
    sections: List[Section]

    @classmethod
    def get_attributes(cls: BaseModel):
        base_attr = cls.__fields__
        attrs = {}
        for key in base_attr:
            type_ = base_attr[key]._type_display()
            if "List" in type_:
                attrs[key] = []  # pragma: no cover
            elif "Dict" in type_:
                attrs[key] = {}  # pragma: no cover
            else:
                attrs[key] = None
        return attrs
