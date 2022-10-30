import json
from app.assets import asset_path


INFO_INDEX = {
    "section_id": {"index": 0, "function": lambda x: x},
    "course_code": {"index": 1, "function": lambda x: x},
    "allow_withdrawal": {
        "index": 2, "function": lambda x: True if x == "SI" else False},
    "english_version": {
        "index": 3, "function": lambda x: True if x == "SI" else False},
    "section": {"index": 4, "function": lambda x: x},
    "need_special_approval": {
        "index": 5, "function": lambda x: True if x == "SI" else False},
    "general_education": {"index": 6, "function": lambda x: x},
    "format": {"index": 7, "function": lambda x: x},
    "category": {"index": 8, "function": lambda x: x},
    "name": {"index": 9, "function": lambda x: x},
    "teacher_name": {"index": 10, "function": lambda x: x},
    "campus": {"index": 11, "function": lambda x: x},
    "value": {"index": 12, "function": lambda x: x},
    "total_vacancies": {"index": 13, "function": lambda x: x},
    "available_vacancies": {"index": 14, "function": lambda x: x}
}

DAYS = {"L": 0, "M": 1, "W": 2, "J": 3, "V": 4, "S": 5, "D": 6}

TRANSLATOR = {}

with open(asset_path('uc_params.json')) as params_file:
    uc_params = json.load(params_file)
    for key in uc_params:
        TRANSLATOR[key] = uc_params[key][-1]
