from typing import List, Optional
from app.models.base import Section, Course, ClassModule


class UCSection(Section):
    allow_withdrawal: bool
    need_special_approval: bool
    general_education: Optional[str]
    category: Optional[str]
    modules: List[ClassModule]


class UCCourse(Course):
    sections: List[UCSection]
