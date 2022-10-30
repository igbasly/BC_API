from typing import List, Optional
from app.models.base import (
    Section,
    Course,
    ClassModule,
    CourseRequirements,
    CourseRequirement,
    CourseRequirementRelation
)


class UCSection(Section):
    allow_withdrawal: bool
    need_special_approval: bool
    general_education: Optional[str]
    category: Optional[str]
    modules: List[ClassModule]


class UCCourseRequirements(CourseRequirements):
    equivalencies: List[CourseRequirementRelation | CourseRequirement]


class UCCourse(Course):
    sections: List[UCSection]
    requirements: Optional[UCCourseRequirements]
