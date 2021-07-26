# BuscaCursos UC REST API  | V1 | INACTIVA |
REST API del sistema BuscaCursos de la PUC Chile.

La versión 1 de la API se encuentra alojada en la url [http://bc.horariomaker.com/api/v1](http://bc.horariomaker.com/api/v1)


## GET
---
### **Requests**

Es una API _read-only_ por lo que solo acepta el método HTTP GET con los siguientes parametros:
* semestre
    - 2018-1
    - 2018-2
    - 2018-3 (TAV verano 2019)
    - 2019-1
    - 2019-2
* sigla
* nrc
* nombre
* profesor
* categoria
* campus
* unidad_academica

Las respuesta son en formato JSON, donde en caso de ser aceptado el *request* contendrá un *key* `data` (`dict`) con todos los cursos donde a su vez, cada curso será otro `dict` con las secciones respectivas y su información correspondiente.

Ejemplo:
```json
{
    'code': 200,
    'status': "OK",
    'data': {
        "IRB2001": {
            "1": {
                "Aprobacion especial":"NO",
                "Campus":"San Joaqu\u00edn",
                "Categoria":null,
                "Creditos":"10",
                "Ingles":"NO",
                "Modulos":{
                    "AYU":[],
                    "CLAS":["M:4,5"],
                    "LAB":["V:5"],
                    "LIB":[],
                    "PRA":[],
                    "SUP":[],
                    "TAL":[],
                    "TER":[],
                    "TES":[]
                    },
                "NRC":"12002",
                "Nombre":"Fundamentos de Rob\u00f3tica",
                "Profesor":"Torres Miguel, Troni Giancarlo, Calabi Daniel, Soto Alvaro",
                "Retiro":"NO",
                "Seccion":"1",
                "Sigla":"IRB2001",
                "Vacantes disponibles":"31",
                "Vacantes totales":"31"}
                }
            }
}
```
*Ejemplo de request `HTTP GET /api/v1?sigla=irb2001`*

---
### **ERRORES**
En caso de `ERROR` la respuesta será en formato JSON de la siguiente forma:
```json
{
    'code':404,
    'status':"Not Found",
    'error':{
        "message":"(#404) Not data found with this parameters."
        }
}
```
*Ejemplo de request `HTTP GET /api/v1?sigla=abc`*

```json
{
    'code':400,
    'status':"Bad Request",
    'error':{
        "invalid_arguments":["foo"],
        "message":"(#400) Some arguments are not accepted."
        }
}
```
*Ejemplo de request `HTTP GET api/v1?foo=pass`*

---
## Ejemplos

Algunos ejemplos de la utilización de esta API mediante python sería:

### Ejemplo 1

```python
import requests

url_api = "http://buscacursos-api.herokuapp.com/api/v1"
params = {
    "sigla": "iic2233",
    "semestre": "2019-2",
    "campus": "TODOS"
    }

response = requests.get(url = url_api, params = params)

print(response.json())
```
Respuesta:
```json
{
    "code": 200,
    "status":"Ok",
    "data": {
        "IIC2233": {
            "1": {
                "Aprobacion especial":"NO",
                "Campus":"San Joaqu\u00edn",
                "Categoria":null,
                "Creditos":"10",
                "Ingles":"NO",
                "Modulos":{
                    "AYU":["M:4"],
                    "CLAS":["J:4,5"],
                    "LAB":[],
                    "LIB":[],
                    "PRA":[],
                    "SUP":[],
                    "TAL":[],
                    "TER":[],
                    "TES":[]
                    },
                "NRC":"12431",
                "Nombre":"Programaci\u00f3n Avanzada",
                "Profesor":"Ruz Cristian",
                "Retiro":"SI",
                "Seccion":"1",
                "Sigla":"IIC2233",
                "Vacantes disponibles":"95",
                "Vacantes totales":"95"
                },
            "2": {
                "Aprobacion especial":"NO",
                "Campus":"San Joaqu\u00edn",
                "Categoria":null,
                "Creditos":"10",
                "Ingles":"NO",
                "Modulos":{
                    "AYU":["M:4"],
                    "CLAS":["J:4,5"],
                    "LAB":[],
                    "LIB":[],
                    "PRA":[],
                    "SUP":[],
                    "TAL":[],
                    "TER":[],
                    "TES":[]
                    },
                "NRC":"15428",
                "Nombre":"Programaci\u00f3n Avanzada",
                "Profesor":"Florenzano Fernando",
                "Retiro":"SI",
                "Seccion":"2",
                "Sigla":"IIC2233",
                "Vacantes disponibles":"95",
                "Vacantes totales":"95"
                },
            "3": {
                "Aprobacion especial":"NO",
                "Campus":"San Joaqu\u00edn",
                "Categoria":null,
                "Creditos":"10",
                "Ingles":"NO",
                "Modulos":{
                    "AYU":["M:4"],
                    "CLAS":["J:4,5"],
                    "LAB":[],
                    "LIB":[],
                    "PRA":[],
                    "SUP":[],
                    "TAL":[],
                    "TER":[],
                    "TES":[]
                    },
                "NRC":"18177",
                "Nombre":"Programaci\u00f3n Avanzada",
                "Profesor":"Ossa Antonio",
                "Retiro":"SI",
                "Seccion":"3",
                "Sigla":"IIC2233",
                "Vacantes disponibles":"95",
                "Vacantes totales":"95"
                }
            }
        }
}
```

### Ejemplo 2
```python
import requests

url_api = "http://buscacursos-api.herokuapp.com/api/v1"
params = {
    "sigla": "PSI1204",
    }

response = requests.post(url = url_api, params = params)

print(response.json())
```

Respuesta:
```json
{
    'code': 405,
    'status': "Method Not Allowed",
    'error': {
        "message": "(#405) This API do not accept PUT or POST methods."
        }
}
```