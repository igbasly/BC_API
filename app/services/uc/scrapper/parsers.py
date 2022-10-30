from typing import Any, Dict, List

from app.models.uc import UCSection, UCCourse, UCCourseRequirements
from app.models.base import (
    ClassModule,
    CourseRequirementRelation,
    CourseRequirement
)
from .constants import INFO_INDEX, DAYS


def parse_class_modules(modules_info) -> List[Dict]:
    modules = []
    if ":" not in modules_info[0] or modules_info[0] == ":":
        return  # pragma: no cover

    days_str, modules_str = modules_info[0].split(":")
    if days_str == "" or modules_str == "":
        return  # pragma: no cover

    for day in days_str.split("-"):
        for mod in modules_str.split(","):
            module = ClassModule.get_attributes()
            module['day'] = DAYS[day]
            module['module'] = int(mod)
            module['type'] = modules_info[1]
            modules.append(module)

    return modules


def parse_section(section_info: List[str]) -> Dict:
    section = UCSection.get_attributes()

    for attr in INFO_INDEX:
        attr_info = INFO_INDEX[attr]
        aux = section_info[attr_info['index']]
        if aux != "":
            section[attr] = attr_info['function'](aux.strip())

    for module_list in section_info[-1]:
        module = parse_class_modules(module_list)
        if module:
            section["modules"].extend(module)

    return section


def parse_search(results: List[Any]):
    courses = {}
    for line in results:
        section_html = []
        for elem in line.find_all("td"):
            if elem.find_all("table"):
                aux = []
                for e in elem.find_all("tr"):
                    mods = e.find_all("td")
                    aux.append([m.get_text().replace("\n", "") for m in mods])
                section_html.append(aux)
                break
            else:
                section_html.append(elem.get_text().replace("\n", ""))

        section = parse_section(section_html)

        if section["course_code"] not in courses:
            course = UCCourse.get_attributes()
            course['name'] = section['name']
            course['course_code'] = section['course_code']
            courses[section["course_code"]] = course

        courses[section["course_code"]]["sections"].append(section)

    return list(courses.values())


def sanitize_and_requirements(info: List[str]) -> List[Dict]:
    new_requirements = CourseRequirementRelation.get_attributes()
    new_requirements['relation'] = "AND"
    info_clean = list(map(lambda s: s.strip("(").strip(")"), info))
    for requirements in info_clean:
        if "Programa=" in requirements:
            req = CourseRequirement.get_attributes()
            req['course_code'] = requirements
        elif " o " in requirements:
            or_relations = requirements.split(" o ")
            req = sanitize_or_requirements(or_relations)
        else:
            req = CourseRequirement.get_attributes()
            req['course_code'] = requirements
        new_requirements['course_codes'].append(req)

    return new_requirements


def sanitize_or_requirements(info: List[str]) -> List[Dict]:
    new_requirements = CourseRequirementRelation.get_attributes()
    new_requirements['relation'] = "OR"
    info_clean = list(map(lambda s: s.strip("(").strip(")"), info))
    for requirements in info_clean:
        if "Programa=" in requirements:
            req = CourseRequirement.get_attributes()
            req['course_code'] = requirements
        elif " y " in requirements:
            and_relations = requirements.split(" y ")
            req = sanitize_and_requirements(and_relations)
        else:
            req = CourseRequirement.get_attributes()
            req['course_code'] = requirements
        new_requirements['course_codes'].append(req)

    return new_requirements


def sanitize_requirement_info(info: str) -> List[str]:
    if info == "No tiene":
        return []

    new_info = []
    if ") o (" in info:
        or_relations = info.split(" o ")
        req = sanitize_or_requirements(or_relations)
    elif ") y (" in info:
        and_relations = info.split(" y ")
        req = sanitize_and_requirements(and_relations)
    elif " o " in info:
        or_relations = info.split(" o ")
        req = sanitize_or_requirements(or_relations)
    elif " y " in info:
        and_relations = info.split(" y ")
        req = sanitize_and_requirements(and_relations)
    else:
        req = CourseRequirement.get_attributes()
        req['course_code'] = info

    new_info.append(req)

    return new_info


def parse_requirement_search(results: List[Any]) -> List[List[str]]:
    requirements = UCCourseRequirements.get_attributes()
    requirements['requirements'] = sanitize_requirement_info(results[0][1])
    requirements['restrictions'] = sanitize_requirement_info(results[2][1])
    requirements['equivalencies'] = sanitize_requirement_info(results[3][1])
    # relations_info = results[1][1].strip()

    return requirements
