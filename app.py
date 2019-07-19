from flask import Flask, request, send_from_directory
import json

from Objects import request_buscacursos

app = Flask(__name__)
#app.config.update(
#    DEBUG=True,
#    SERVER_NAME="192.168.0.15:8080"
#)


with open("info_buscacursos.json", "r") as file:
    INFO = json.load(file)

key_conversor = {
    "semestre": "cxml_semestre",
    "sigla": "cxml_sigla",
    "nrc": "cxml_nrc",
    "nombre": "cxml_nombre",
    "profesor": "cxml_profesor",
    "categoria": "cxml_categoria",
    "campus": "cxml_campus",
    "unidad_academica": "cxml_unidad_academica"
}


def response(code: int, data: dict=None):
    """ Create the response for any request based on the status code.

    Args:
        code (int): Status code of the response
        data (dict): Information to be return in necesary cases.

    Returns:
        dict: Response in dictonary format with all information about the\
            request.
        int: Status code of response.

    Codes:
        200: "Ok"
        201: "Created"
        202: "Accepted"
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
        201: "Created",
        202: "Accepted",
        204: "No Content",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }

    response_template = {
        "code": code,
        "status": codes[code]
    }

    if code//400 >= 1:
        response_template["error"] = data
    else:
        response_template["data"] = data

    return response_template, code


@app.route("/api/v1", methods=["GET"])
def BC_API_get():
    parameters = {
        "cxml_semestre": "2019-2",
        "cxml_sigla": "",
        "cxml_nrc": "",
        "cxml_nombre": "",
        "cxml_profesor": "",
        "cxml_categoria": "TODOS",
        "cxml_campus": "TODOS",
        "cxml_unidad_academica": "TODOS"
    }

    arguments = request.args
    bad_arguments = []
    for a in arguments:
        if a not in key_conversor:
            bad_arguments.append(a)
            continue
        parameters[key_conversor[a]] = "+".join(arguments[a].split(" "))
    if bad_arguments:
        return response(400,
                        {"message": "(#400) Some arguments are not accepted.",
                         "invalid_arguments": bad_arguments})

    try:
        data_courses = request_buscacursos(parameters)
    except Exception as exc:
        return response(500, {
            "message": "(#500) An internal error ocurred, we are working on it."
            })

    if len(data_courses) > 0:
        return response(200, data_courses)
    return response(404, {
        "message": "(#404) Not data found with this parameters."})


@app.route("/api/v1", methods=["POST", "PUT"])
def BC_API_post():
    return response(405, {
        "message": "(#405) This API do not accept the PUT or POST methods."})


@app.route("/favicon.ico", methods=["GET"])
def icon():
    return send_from_directory("Files", "favicon.png")


if __name__ == "__main__":
    app.run()
