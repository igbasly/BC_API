import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.error import HTTPError
from urllib.parse import urlencode

from app.assets import asset_path
from .parsers import (
    parse_search,
    parse_requirement_search,
    parse_vacancy_search
)


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

    except HTTPError:  # pragma: no cover
        search = []  # pragma: no cover

    courses = parse_search(search)

    return courses


def request_requirements(sigla: str) -> List[Dict]:
    """Assamble the url with the course code of interest, request the url to UC
    server and parse the response into an array of Requirements model.
    Args:
        sigla (str): Course code of interest.
    Returns:
        List: Arrays of UCCourseRequirements dicts.
    """
    url = (
        "http://catalogo.uc.cl/index.php?tmpl=component&"
        f"option=com_catalogo&view=requisitos&sigla={sigla.upper()}"
    )
    try:
        resp = requests.get(url).text

        soup = BeautifulSoup(resp, "lxml")

        search = soup.find_all(
            "table", attrs={"class": "tablesorter tablesorter-blue"})
    except HTTPError:
        search = []

    results = []  # pragma: no cover
    for line in search:
        line = line.get_text().split("\n")
        remove = []
        for i in range(len(line)):
            line[i] = line[i].replace("\t", "")
            if line[i] == "":
                remove.append(i - len(remove))
        for i in remove:
            line.pop(i)
        result = [row.split("\xa0\xa0") for row in line]
        results.extend(result)

    parsed_results = parse_requirement_search(results)

    return parsed_results


def request_vacancies(semester: str, section_id: int) -> List[Dict]:
    """Make the requests for vacancies to BuscaCursos serves and format the
    info into the API response format to vancany.
    Args:
        semester (str): Semester code of interest.
        section_id (int): The nrc code from a specific section of a course.
            This need to be a valid nrc from the semestre requested.
    Returns:
        dict: Dict with the vacancy information of the section given in the API
        response format.
    """
    url = (
        "http://buscacursos.uc.cl/informacionVacReserva"
        f".ajax.php?nrc={section_id}&termcode={semester}"
    )
    try:
        search = request_table_url(url)
    except HTTPError:
        search = []

    results = parse_vacancy_search(search)

    return results
