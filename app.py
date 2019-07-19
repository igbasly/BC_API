from flask import Flask, request
import json

from Objects import request_curso

app = Flask(__name__)
app.debug = True


with open("info_buscacursos.json", "r") as file:
    INFO = json.load(file)


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


@app.route("/api/v1", methods=["GET"])
def get():
    parameters = {
        "cxml_semestre": list(INFO["semestres"].values())[-1],
        "cxml_sigla": "",
        "cxml_nrc": "",
        "cxml_nombre": "",
        "cxml_profesor": "",
        "cxml_categoria": "TODOS",
        "cxml_campus": "TODOS",
        "cxml_unidad_academica": "TODOS"
    }
    arguments = request.args
    for p in arguments:
        if p not in parameters_transform:
            return f"Bad Request: parameter {p}.", 400
        parameters[parameters_transform[p]] = arguments[p]
    web_response = request_curso(parameters)
    if len(web_response) > 0:
        return web_response, 200
    return "Items not found", 40


@app.route("/api/v1", methods=["POST", "PUT"])
def put():
    return "Method Not Allowed", 405


if __name__ == "__main__":
    app.run()
