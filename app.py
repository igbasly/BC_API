from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS
import json

from Requests import request_buscacursos, request_vacancy, request_requirements


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


with open("info_buscacursos.json", "r") as file:
    INFO = json.load(file)

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


def response(code: int, data: dict = None):
    """ Create the response for any request based on the status code.

    Args:
        code (int): Status code of the response
        data (dict): Information to be returned if required.

    Returns:
        dict: Response in dictionary format with all the information about the\
            request.
        int: Status code of response.

    Codes:
        200: "Ok"
        204: "No Content"
        400: "Bad Request"
        403: "Forbidden"
        404: "Not Found"
        405: "Method Not Allowed"
        500: "Internal Server Error"
        503: "Service Unavailable"
    """

    codes = {
        200: "Ok",
        202: "Accepted",
        204: "No Content",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
        503: "Service Unavailable",
    }

    response_template = {"code": code, "status": codes[code]}

    if code // 400 >= 1:
        response_template["error"] = data
    else:
        response_template["data"] = data
    return response_template, code


@app.route("/favicon.ico", methods=["GET"])
def icon():
    """ Return the favicon for explorers
    Returns:
        'Favicon' file
    """
    return send_from_directory("Files", "favicon.png")

@app.route("/", methods=["GET"])
def index():

    return redirect("https://igbasly.github.io/BC_API")


@app.route("/api/v1", methods=["GET"])
def BC_API_get(vacantes=False, formato=False, formacion_general=False):
    """ HTTP GET method for v1
    Args:
        vancante (bool): Allow the use of 'vacantes' parameters in the request.

    Returns:
        dict: Response in dictionary format with all information about the\
            request.
        int: Status code of response.

    """
    parameters = {
        "cxml_semestre": "2019-2",
        "cxml_sigla": "",
        "cxml_nrc": "",
        "cxml_nombre": "",
        "cxml_profesor": "",
        "cxml_categoria": "TODOS",
        "cxml_campus": "TODOS",
        "cxml_unidad_academica": "TODOS",
    }
    arguments = request.args
    bad_arguments = []
    if not arguments:
        return response(400, {"message": "(#400) Requests with no arguments."})
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
        parameters[KEY_CONVERSOR[a]] = "+".join(arguments[a].split(" "))
    if bad_arguments:
        return response(
            400,
            {
                "message": "(#400) Some arguments are not accepted.",
                "invalid_arguments": bad_arguments,
            },
        )

    try:
        data_classes = request_buscacursos(parameters)
    except Exception as exc:
        print(exc)
        return response(
            500, {"message": "(#500) An internal error ocurred, we are working on it."}
        )

    if len(data_classes) > 0:
        return response(200, data_classes)

    return response(202, {"message": "(#202) No data found with those parameters."})


@app.route("/api/v1", methods=["POST", "PUT", "PATCH", "DELETE"])
@app.route("/api/v2", methods=["POST", "PUT", "PATCH", "DELETE"])
@app.route("/api/v3", methods=["POST", "PUT", "PATCH", "DELETE"])
def BC_API_post():
    return response(
        405, {"message": "(#405) This API does not accept PUT or POST methods."}
    )


@app.route("/api/v2", methods=["GET"])
def BC_API_v2_get():
    """ HTTP GET method for v2
    This methods allows use of 'vacantes' parameter in the request.

    Returns:
        dict: Response in dictonary format with all information about the\
            request.
        int: Status code of response.
    """

    resp, code = BC_API_get(True)
    if "vacantes" in request.args and code == 200:
        if request.args["vacantes"] == "true":
            for cla in resp["data"].values():
                for sec in cla.values():
                    vacancy = request_vacancy(sec["NRC"], sec["Semestre"])
                    sec["Vacantes"] = vacancy
                    total = sec.pop("Vacantes totales")
                    sec["Vacantes"]["Totales"] = total
                    available = sec.pop("Vacantes disponibles")
                    sec["Vacantes"]["Disponibles"] = available
        elif request.args["vacantes"] != "false":
            return response(
                400,
                {
                    "message": "(#400) Parameter 'vacantes' "
                    + "only accepts boolean values."
                },
            )
    return resp, code


@app.route("/api/v3", methods=["GET"])
def BC_API_v3_get():
    """ HTTP GET method for v3
    This method allows the use of 'requisitos' parameter in the request.

    Return:
        dict: Response in dictionary format with all information about the\
            request.
        int: Status code of response.
    """
    vac = False
    form = False
    if "vacantes" in request.args and request.args["vacantes"] not in ["true", "false"]:
        return response(
            400,
            {
                "message": "(#400) Parameter 'requisitos' " +
                "only accepts boolean values."
            }
        )
    elif "vacantes" in request.args and request.args["vacantes"] == "true":
        vac = True
    if "formato" in request.args and request.args["formato"] not in ["true", "false"]:
            return response(
                400,
                {
                    "message": "(#400) Parameter 'formato' " +
                    "only accept boolean values."
                }
            )
    elif "formato" in request.args and request.args["formato"] == "true":
        form = True
    if "requisitos" in request.args and request.args["requisitos"] not in [
        "true",
        "false",
    ]:
            return response(
                400,
                {
                    "message": "(#400) Parameter 'requisitos' " +
                    "only accepts boolean values."
                }
            )

    resp, code = BC_API_get(vac, form, True)

    if "vacantes" in request.args and code == 200:
        if vac:
            for cla in resp["data"].values():
                for sec in cla.values():
                    vacancy = request_vacancy(sec["NRC"], sec["Semestre"])
                    sec["Vacantes"] = vacancy
                    total = sec.pop("Vacantes totales")
                    sec["Vacantes"]["Totales"] = total
                    available = sec.pop("Vacantes disponibles")
                    sec["Vacantes"]["Disponibles"] = available
    if "requisitos" in request.args and code == 200:
        if request.args["requisitos"] == "true":
            for sigla in resp["data"]:
                req = request_requirements(sigla)
                resp["data"][sigla]["Requisitos"] = req
    return resp, code


@app.route("/api/v3/requisitos", methods=["GET"])
def BC_API_v3_req_get():
    """ HTTP GET method for v3 with 'requisitos' scope.
    This method returns course requisities associated with an identifier.

    Return:
        dict: Response in dictonary format with all information about the\
            request.
        int: Status code of response.
    """
    denied = []
    sigla = ""
    for a in request.args:
        if a == "sigla":
            sigla = request.args[a]
        else:
            denied.append(a)
    if len(denied) != 0:
        return response(
            405, {"message": f"(#405) Parameters {', '.join(denied)} are not accepted."}
        )
    if not sigla:
        return response(400, {"message": "(#400) No value for the 'sigla' parameter."})

    info = request_requirements(sigla)

    i = 0
    for value in info.values():
        if not value:
            i += 1
            break

    if not i:
        return response(202, {"message": "(#202) No data found with these parameters."})

    return response(200, {sigla: info})


if __name__ == "__main__":
    app.run(debug=False)
