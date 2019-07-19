from flask_restful import Resource
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import json
import urllib.request


with open("info_buscacursos.json", "r") as file:
    INFO = json.load(file)


def ask_url(url):
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


def request_curso(params):
    web = f"http://buscacursos.uc.cl/?" \
          f"{'&'.join(e + '=' + params[e] for e in params)}&cxml_horario_" \
          f"tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad" \
          f"=TODOS#resultados"
    #print(web)
    try:
        search = ask_url(web)
    except HTTPError:

        search = []
    info_index = {"NRC": 1, "Sigla": 2, "Retiro": 3, "Ingles": 4, "Seccion": 5,
                  "Aprobacion especial": 6, "Categoria": 8}
    info_index2 = {"Nombre": 9, "Profesor": 10, "Campus": 11, "Creditos": 12,
                   "Vacantes totales": 13, "Vacantes disponibles": 14}
    info_index3 = {"Nombre": 11, "Profesor": 12, "Campus": 13, "Creditos": 14,
                   "Vacantes totales": 15, "Vacantes disponibles": 16}
    cursos = dict()
    for e in search:
        seccion_html = e.get_text().split("\n")
        info = {"NRC": None, "Sigla": None, "Retiro": None, "Ingles": None,
                "Seccion": None, "Aprobacion especial": None,
                "Categoria": None, "Nombre": None, "Profesor": None,
                "Campus": None, "Creditos": None, "Vacantes totales": None,
                "Vacantes disponibles": None,
                "Modulos": {"CLAS": [], "AYU": [], "LAB": [], "LIB": [],
                            "PRA": [], "SUP": [], "TAL": [], "TER": [],
                            "TES": []}}
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
        
        cursos[info["sigla"]] = info

    return cursos


class BuscaCursos(Resource):

    parameters_transform = {
        "semestre": "cxml_semestre",
        "sigla": "cxml_sigla",
        "nrc": "cxml_nrc",
        "nombre": "cxml_nombre",
        "profesor": "cxml_profesor",
        "categoria": "cxml_categoria",
        "campus": "cxml_campus",
        "unidad_academica": "cxml_unidad_academica"
    }

    def get(self, params):
        parameters = {
            "cxml_semestre": INFO["semestres"].values()[-1],
            "cxml_sigla": "",
            "cxml_nrc": "",
            "cxml_nombre": "",
            "cxml_profesor": "",
            "cxml_categoria": "TODOS",
            "cxml_campus": "TODOS",
            "cxml_unidad_academica": "TODOS"
        }
        params = params.strip("?").split("&")
        request = dict()
        for p in params:
            parameter, value = p.split("=")
            request[parameter] = value

        for parameter in request:
            if parameter not in self.parameters_transform:
                return f"Bad Request: parameter {parameter}.", 400
            parameters[self.parameters_transform[parameter]] =\
                request[parameter]

        web_response = request_curso(parameters)
        if len(web_response) > 0:
            return web_response, 200
        return "Items not found", 404

    def put(self, params):
        return "Method Not Allowed", 405
