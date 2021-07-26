from Requests import request_vacancy, request_requirements


KEY_CONVERSOR = {
    "semestre": "cxml_semestre",
    "sigla": "cxml_sigla",
    "nrc": "cxml_nrc",
    "nombre": "cxml_nombre",
    "profesor": "cxml_profesor",
    "categoria": "cxml_categoria",
    "campus": "cxml_campus",
    "unidad_academica": "cxml_unidad_academica",
    "vacantes": "vacantes",
    "requisitos": "requisitos",
    "formato": "cxml_formato_cur",
    "formacion_general": "cxml_area_fg"
}


def check_arguments(arguments, vacantes, formato, formacion_general):
    parameters = {
        "cxml_semestre": "2021-2",
        "cxml_sigla": "",
        "cxml_nrc": "",
        "cxml_nombre": "",
        "cxml_profesor": "",
        "cxml_categoria": "TODOS",
        "cxml_campus": "TODOS",
        "cxml_unidad_academica": "TODOS",
    }

    bad_arguments = []

    for a in arguments:
        if a not in KEY_CONVERSOR:
            bad_arguments.append(a)
            continue
        elif a == "vacantes":
            if not vacantes:
                bad_arguments.append(a)
            continue
        elif a == "formato":
            if not formato:
                bad_arguments.append(a)
            parameters[KEY_CONVERSOR[a]] = "TODOS"
            continue
        elif a == "formacion_general":
            if not formacion_general:
                bad_arguments.append(a)
            parameters[KEY_CONVERSOR[a]] = "TODOS"
            continue

        parameters[KEY_CONVERSOR[a]] = arguments[a]

    return parameters, bad_arguments


def manage_vacancies(results):
    new_results = {}

    for sig, cla in results.items():
        new_class = cla.copy()
        for n_sec, sec in cla.items():
            new_sec = sec.copy()
            vacancy = request_vacancy(sec["NRC"], sec["Semestre"])
            new_sec["Vacantes"] = vacancy
            total = new_sec.pop("Vacantes totales")
            new_sec["Vacantes"]["Totales"] = total
            available = new_sec.pop("Vacantes disponibles")
            new_sec["Vacantes"]["Disponibles"] = available
            new_class[n_sec] = new_sec
        results[sig] = new_class

    return new_results


def manage_requirements(results):
    new_results = {}

    for sigla in results:
        new_class = results[sigla]
        req = request_requirements(sigla)
        new_class["Requisitos"] = req
        new_results[sigla] = new_class

    return new_results
