from flask_restful import Resource
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import json
import urllib.request


def request_url(url):
    resp = urllib.request.urlopen(url)

    soup = BeautifulSoup(resp, "lxml")

    name_box = soup.find_all('tr', attrs={'class': 'resultadosRowPar'})
    name_box1 = soup.find_all('tr', attrs={'class': 'resultadosRowImpar'})

    result = []

    for i in range((len(name_box) + len(name_box1))):
        if name_box and i % 2 == 0:
            result.append(name_box.pop(0))
        elif name_box1 and i % 2 != 0:
            result.append(name_box1.pop(0))
    return result


def request_buscacursos(params):
    url = f"http://buscacursos.uc.cl/?" \
          f"{'&'.join(e + '=' + params[e] for e in params)}&cxml_horario_" \
          f"tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad" \
          f"=TODOS#resultados"
    try:
        search = request_url(url)
    except HTTPError:

        search = []
    info_index = {"NRC": 1, "Sigla": 2, "Retiro": 3, "Ingles": 4, "Seccion": 5,
                  "Aprobacion especial": 6, "Categoria": 8}
    info_index2 = {"Nombre": 9, "Profesor": 10, "Campus": 11, "Creditos": 12,
                   "Vacantes totales": 13, "Vacantes disponibles": 14}
    info_index3 = {"Nombre": 11, "Profesor": 12, "Campus": 13, "Creditos": 14,
                   "Vacantes totales": 15, "Vacantes disponibles": 16}
    cursos = dict()
    for line in search:
        seccion_html = line.get_text().split("\n")

        info = {
            "NRC": None,
            "Semestre": params["cxml_semestre"],
            "Sigla": None,
            "Seccion": None,
            "Retiro": None,
            "Ingles": None,
            "Aprobacion especial": None,
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
                "TES": []
                }
            }

        for i in info_index:
            aux = seccion_html[info_index[i]]
            if aux != "":
                info[i] = aux.strip()

        if info["Categoria"]:
            info_index_aux = info_index3
        else:
            info_index_aux = info_index2

        for i in info_index_aux:
            aux = seccion_html[info_index_aux[i]]
            if aux != "":
                info[i] = aux.strip()

        mod = info["Modulos"]
        i = info_index_aux["Vacantes disponibles"] + 6

        while True:
            modulos = seccion_html[i]
            if modulos in ["", ":"]:
                break
            tipo = seccion_html[i + 3]
            i += 11
            mod[tipo].append(modulos)

        if info["Sigla"] not in cursos:
            cursos[info["Sigla"]] = {info["Seccion"]: info}

        cursos[info["Sigla"]][info["Seccion"]] = info

    return cursos


def request_vacancy(nrc: str, semester: str):
    url = f"http://buscacursos.uc.cl/informacionVacReserva" +\
          f".ajax.php?nrc={nrc}&termcode={semester}"
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
        seccion_html = [s.strip(" ") for s in seccion_html[0].split("-")] +\
            seccion_html[1:]
        results.append(seccion_html)
    results = results[1:] if len(results) > 0 else []
    finals = {"Disponibles": 0}
    for esc in results:
        if len(esc) < 3:
            continue
        if esc[0] == "Vacantes libres" or esc[0] == "Vacantes Libres":
            if len(esc) == 4:
                finals["Libres"] = [int(i) for i in esc[-3:]]
            else:
                aux = [int(i) for i in esc[len(esc)-3:]]
                for i in range(3):
                    finals["Libres"][i] += aux[i]
            continue
        elif "TOTAL DISPONIBLES" in esc[0]:
            finals["Disponibles"] = int(esc[1])
            continue
        finals[esc[0]] = [int(i) for i in esc[-3:]]
    return finals


def request_requirements(sigla: str):
    url = f"http://catalogo.uc.cl/index.php?tmpl=component&" +\
          f"option=com_catalogo&view=requisitos&sigla={sigla.upper()}"
    try:
        resp = urllib.request.urlopen(url)

        soup = BeautifulSoup(resp, "lxml")

        search = soup.find_all('table',
                               attrs={'class': 'tablesorter tablesorter-blue'})
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
        "Restricciones": []
        }

    if results:
        response["Prerequisitos"] = results[0][1]
        response["Relacion entre prerequisitos y restricciones"] = results[1][1]
        response["Restricciones"] = results[2][1]
        response["Equivalencias"] = results[3][1]

    return response
