from urllib.request import HTTPError
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests_functions import parse_search, parse_vacancy_search, parse_vacancy_results
import requests


"""
Requests module

Handle the url requests from BuscaCursos page, the scrape work to get all the
data and assable the json structure to return.
"""


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


def request_buscacursos(params):
    """Assamble the BuscaCursos url and make the requests. In case of a valid
    response, clean all the information and put them on a dict with the API
    format response.

    Args:
        params (dict): Dict with valid BuscaCursos requests parameters.

    Returns:
        dict: Dict with courses data response in API format.
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

    courses = parse_search(params, search)

    return courses


def request_vacancy(nrc: str, semester: str):
    """Make the requests for vacancies to BuscaCursos serves and format the
    info into the API response format to vancany.

    Args:
        nrc (str): The nrc code from a specific section of a course. This
        need to be a valid nrc from the semestre requested.
        semester (str): Semester code of interes.

    Returns:
        dict: Dict with the vacancy information of the section given in the API
        response format.
    """
    url = (
        "http://buscacursos.uc.cl/informacionVacReserva"
        f".ajax.php?nrc={nrc}&termcode={semester}"
    )
    try:
        search = request_table_url(url)
    except HTTPError:
        search = []

    results = parse_vacancy_search(search)
    results = results[1:] if len(results) > 0 else []

    finals = parse_vacancy_results(results)

    return finals


def request_requirements(sigla: str):
    """Assamble the url with the course code of interest, request the url to UC
    server and parse the response into a dict with the API response format.

    Args:
        sigla (str): Course code of interest.

    Returns:
        dict: Dict with course requirements in API response format.
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

    results = []
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

    for item in results:
        item[1] = item[1].strip(")").strip("(").split(" o ")
        item[1] = [s.strip(")").strip("(").split(" y ") for s in item[1]]
        item[1] = [s if len(s) != 1 else s[0] for s in item[1]]
        if item[1][0] == "No tiene":
            item[1] = []

    response = {
        "Relacion entre prerequisitos y restricciones": [],
        "Prerequisitos": [],
        "Equivalencias": [],
        "Restricciones": [],
    }

    if results:
        response["Prerequisitos"] = results[0][1]
        response["Relacion entre prerequisitos y restricciones"] = results[1][1]
        response["Restricciones"] = results[2][1]
        response["Equivalencias"] = results[3][1]

    return response
