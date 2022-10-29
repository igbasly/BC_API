from typing import List, Optional
from app.models.base import Section, Course, ClassModules


class UCSection(Section):
    allow_withdrawal: bool
    need_special_approval: bool
    general_education: Optional[str]
    category: Optional[str]
    modules: Optional[List[ClassModules]]


class UCCourse(Course):
    sections: List[UCSection]
