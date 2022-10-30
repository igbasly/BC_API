import requests
import json
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.parse import urlencode

from app.assets import asset_path
from .parsers import parse_search


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
