INFO_INDEX = {
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


def generate_template():
    return {
        "NRC": None,
        "Semestre": None,
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


def parse_search(params, results):
    courses = dict()
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

        info = generate_template()
        info["Semestre"] = params["cxml_semestre"]

        for i in INFO_INDEX:
            aux = section_html[INFO_INDEX[i]]
            if aux != "":
                info[i] = aux.strip()

        for list_ in section_html[-1]:
            info["Modulos"][list_[1]].append(list_[0])

        if info["Sigla"] not in courses:
            courses[info["Sigla"]] = {info["Seccion"]: info}

        courses[info["Sigla"]][info["Seccion"]] = info

    return courses


def parse_vacancy_search(search):
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

    return results


def parse_vacancy_results(results):
    finals = {"Disponibles": 0}

    for esc in results:
        if len(esc) < 3:
            continue
        print(esc)
        if esc[0] == "Vacantes libres" or esc[0] == "Vacantes Libres":
            if len(esc) == 4:
                finals["Libres"] = [int(i) for i in esc[-3:]]
            else:
                aux = [int(i) for i in esc[len(esc) - 3:]]
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
