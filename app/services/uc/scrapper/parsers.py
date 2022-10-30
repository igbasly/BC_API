from typing import Any, Dict, List

from app.models.uc import UCSection, UCCourse
from app.models.base import ClassModule
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
