from urllib.request import HTTPError
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import urllib.request
import unicodedata


"""
Requests module

Handle the url requests from BuscaCursos page, the scrape work to get all the
data and assable the json structure to return.
"""


def request_url(url):
    """Make the requests to BuscaCursos server and parse the xml response to
    separete all the results in a single list.

    Args:
        url (str): A valid complete BuscaCursos url.

    Returns:
        list: List with sublists with all the contents of BuscaCursos reponse.
    """
    resp = urllib.request.urlopen(url)

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

    url = (
        f"http://buscacursos.uc.cl/?"
        f"{urlencode(params)}#resultados"
    )
    try:
        search = request_url(url)

    except HTTPError:
        search = []
 
    info_index = {
        "NRC": 0,
        "Sigla": 1,
        "Retiro": 2,
        "Ingles": 3,
        "Seccion": 4,
        "Aprobacion especial": 5,
        "Area de FG": 6,
        "Formato": 7,
        "Categoria": 8,
        "Nombre": 9,
        "Profesor": 10,
        "Campus": 11,
        "Creditos": 12,
        "Vacantes totales": 13,
        "Vacantes disponibles": 14
    }

    cursos = dict()
    for line in search:
        seccion_html = []
        for elem in line.find_all("td"):
            if elem.find_all("table"):
                aux = []
                for e in elem.find_all("tr"):
                    mods = e.find_all("td")
                    aux.append([m.get_text().replace("\n", "") for m in mods])
                seccion_html.append(aux)
                break
            else:
                seccion_html.append(elem.get_text().replace("\n", ""))
        print(seccion_html)

        info = {
            "NRC": None,
            "Semestre": params["cxml_semestre"],
            "Sigla": None,
            "Seccion": None,
            "Retiro": None,
            "Ingles": None,
            "Aprobacion especial": None,
            "Area de FG": None,
            "Formato": None,
            "Categoria": None,
            "Nombre": None,
            "Profesor": None,
            "Campus": None,
            "Creditos": None,
            "Vacantes totales": None,
            "Vacantes disponibles": None,
            "Modulos": {
                "CLAS": [],
                "AYU": [],
                "LAB": [],
                "LIB": [],
                "PRA": [],
                "SUP": [],
                "TAL": [],
                "TER": [],
                "TES": [],
            },
        }

        for i in info_index:
            aux = seccion_html[info_index[i]]
            if aux != "":
                info[i] = aux.strip()

        for list_ in seccion_html[-1]:
            info["Modulos"][list_[1]].append(list_[0])

        if info["Sigla"] not in cursos:
            cursos[info["Sigla"]] = {info["Seccion"]: info}

        cursos[info["Sigla"]][info["Seccion"]] = info

    return cursos


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
        f"http://buscacursos.uc.cl/informacionVacReserva"
        + f".ajax.php?nrc={nrc}&termcode={semester}"
    )
    try:
        search = request_url(url)
    except HTTPError:
        search = []

    results = []
    for line in search:
        seccion_html = line.get_text().split("\n")
        remove = []
        for i in range(len(seccion_html)):
            seccion_html[i] = seccion_html[i].replace("\t", "")
            if seccion_html[i] == "":
                remove.append(i - len(remove))
        for i in remove:
            seccion_html.pop(i)
        seccion_html = [
            s.strip(" ") for s in seccion_html[0].split("-")
        ] + seccion_html[1:]
        results.append(seccion_html)
    results = results[1:] if len(results) > 0 else []
    finals = {"Disponibles": 0}
    for esc in results:
        if len(esc) < 3:
            continue
        print(esc)
        if esc[0] == "Vacantes libres" or esc[0] == "Vacantes Libres":
            if len(esc) == 4:
                finals["Libres"] = [int(i) for i in esc[-3:]]
            else:
                aux = [int(i) for i in esc[len(esc) - 3 :]]
                for i in range(3):
                    if finals.get("Libre"):
                        finals["Libres"][i] += aux[i]
                    else:
                        finals["Libres"] = aux[i]
            continue
        elif "TOTAL DISPONIBLES" in esc[0]:
            finals["Disponibles"] = int(esc[1])
            continue
        finals[esc[0]] = [int(i) for i in esc[-3:]]
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
        f"http://catalogo.uc.cl/index.php?tmpl=component&"
        + f"option=com_catalogo&view=requisitos&sigla={sigla.upper()}"
    )
    try:
        resp = urllib.request.urlopen(url)

        soup = BeautifulSoup(resp, "lxml")

        search = soup.find_all("table", attrs={"class": "tablesorter tablesorter-blue"})
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
