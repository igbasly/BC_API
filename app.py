from flask import Flask
from flask_restful import Api

from Objects import BuscaCursos

app = Flask(__name__)
api = Api(app)

api.add_resource(BuscaCursos, "/BuscaCursosAPI/v1/<str:params>")


if __name__ == "__main__":
    app.run()
