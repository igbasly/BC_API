import requests
import json
from copy import deepcopy
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.parse import urlencode

from app.assets import asset_path
from .constants import INFO_INDEX, SECTION_BASE, COURSE_BASE, MODULE_BASE, DAYS
from app.models.base import ClassModule


def request_table_url(url):
    """Make the requests to BuscaCursos server and parse the xml response to
    separete all the results in a single list.
    Args:
        url (str): A valid complete BuscaCursos url.
    Returns:
        list: List with sublists with all the contents of BuscaCursos reponse.
    """
    resp = requests.get(url).text

    soup = BeautifulSoup(resp, "lxml")

    name_box = soup.find_all("tr", attrs={"class": "resultadosRowPar"})
    name_box1 = soup.find_all("tr", attrs={"class": "resultadosRowImpar"})

    result = []

    for i in range((len(name_box) + len(name_box1))):
        if name_box and i % 2 == 0:
            result.append(name_box.pop(0))
        elif name_box1 and i % 2 != 0:
            result.append(name_box1.pop(0))
    return result


def request_parameters():
    """Make the requests to BuscaCursos server and parse the xml response to
    separete all the parameters in a single object.
    Returns:
        dict: Object with all accepted paramters and its options values and
              names.
    """
    resp = requests.get("http://buscacursos.uc.cl/").text

    soup = BeautifulSoup(resp, "lxml")

    with open(asset_path('uc_params.json'), "r") as file_:
        params_names = json.load(file_)

    parameters = []

    for param in params_names:
        info = params_names[param]
        resource = {"name": param, "type": info[0]}
        if info[0] == "select":
            selects = soup.find_all("select", attrs={"name": info[1]})
            options = []
            if selects:
                select = selects[0]
                options_html = select.find_all("option")
                for op in options_html:
                    option = {"value": op["value"], "name": op.get_text()}
                    options.append(option)
            resource["values"] = options

        parameters.append(resource)

    return parameters


def parse_search(results):
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

        section = deepcopy(SECTION_BASE)

        for attr in INFO_INDEX:
            attr_info = INFO_INDEX[attr]
            aux = section_html[attr_info['index']]
            if aux != "":
                section[attr] = attr_info['function'](aux.strip())

        for list_ in section_html[-1]:
            print(section["name"], list_)
            if ":" not in list_[0] or list_[0] == ":":
                continue

            days_str, modules_str = list_[0].split(":")
            if days_str == "" or modules_str == "":
                continue

            for day in days_str.split("-"):
                for mod in modules_str.split(","):
                    module = deepcopy(MODULE_BASE)
                    module['day'] = DAYS[day]
                    module['module'] = int(mod)
                    module['type'] = list_[1]
                    section["modules"].append(module)

        if section["course_code"] not in courses:
            course = deepcopy(COURSE_BASE)
            course['name'] = section['name']
            course['course_code'] = section['course_code']
            courses[section["course_code"]] = course

        courses[section["course_code"]]["sections"].append(section)

    return list(courses.values())


def request_buscacursos(params):
    """Assamble the BuscaCursos url and make the requests. In case of a valid
    response, clean all the information and put them on a dict with the API
    format response.
    Args:
        params (dict): Dict with valid BuscaCursos requests parameters.
    Returns:
        list: List of courses data response in API format.
    """
    params.update(
        {
            "cxml_horario_tipo_busqueda": "si_tenga",
            "cxml_horario_tipo_busqueda_actividad": "TODOS",
        }
    )

    url = f"http://buscacursos.uc.cl/?{urlencode(params)}#resultados"

    try:
        search = request_table_url(url)

    except HTTPError:
        search = []

    courses = parse_search(search)

    return courses
