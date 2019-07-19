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
            "Sigla": None,
            "Retiro": None,
            "Ingles": None,
            "Seccion": None,
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
