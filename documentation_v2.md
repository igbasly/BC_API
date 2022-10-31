# BuscaCursos UC REST API  | V2 | (_DEPRECATED_) 
REST API del sistema BuscaCursos de la PUC Chile.

La versión 2 de la API se encuentra alojada en la url [http://bc.horariomaker.com/api/v2](http://bc.horariomaker.com/api/v2)


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
* vacantes
    - true
    - false

Las respuesta son en formato JSON, donde en caso de ser aceptado el *request* contendrá un *key* `data` (`dict`) con todos los cursos donde a su vez, cada curso será otro `dict` con las secciones respectivas y su información correspondiente.

Ejemplo:
```json
{
    'code': 200,
    'status': "OK",
    'data': {
        "ICC2304": {
            "1": {
                "Aprobacion especial":"NO",
                "Campus":"San Joaqu\u00edn",
                "Categoria":null,
                "Creditos":"10",
                "Ingles":"NO",
                "Modulos":{
                    "AYU":[],
                    "CLAS":["M-J:2"],
                    "LAB":[],
                    "LIB":[],
                    "PRA":[],
                    "SUP":[],
                    "TAL":[],
                    "TER":["V:1,2,3"],
                    "TES":[]
                    },
                "NRC":"10659",
                "Nombre":"Ingenier\u00eda de Construcci\u00f3n",
                "Profesor":"Vera Sergio, Carpio Manuel",
                "Retiro":"NO",
                "Seccion":"1",
                "Sigla":"ICC2304",
                "Semestre": "2019-2",
                "Vacantes": {
                    "Libres": [100, 76, 24],
                    "Disponibles": 24,
                    "Totales": 100
                    }
                }
            }
        }
}
```
*Ejemplo de request `HTTP GET /api/v2?sigla=ICC2304`*

---
### **Vacantes**

En caso de utilizarse el parametro `vacantes`, el cual solo permite el uso de un booleano como valor *(true o false)*, la respuesta inluirá para cada **sección** un *keyword* **Vacantes** que corresponde a un diccionario con las vacantes reservadas para las distintas **unidades** representadas por su código o **Libres** junto con el **total disponible** y el **total de vacantes**.

Un ejemplo mas detallado podría verse:
```json
...

"Vacantes": {
    "04": [83,83,0],
    "06": [4,4,0],
    "09": [7,7,0],
    "Libres": [15,15,0],
    "Disponibles": "0",
    "Totales": "109"
},

...
```

Donde `04` es el código de **Ingeniería**, `06` de **Matemáticas** y 09 de **College**.

Por otro lado, las vacantes que cada uno de estos incluye se detallan como:

<table>
<tr>
<th> </th>
<th> Ofrecidas </th>
<th> Ocupadas </th>
<th> Disponibles </th>
</tr>
<tr> <td>04 - Ingeniería </td><td>83</td><td>83</td><td>0</td></tr>
<tr><td>06 - Matemáticas </td><td> 4</td><td>4</td><td>0</td></tr>
<tr><td>09 - College </td><td> 7 </td><td>7 </td><td>0</td></tr>
<tr><td>Libres</td><td> 15 </td><td>15 </td><td>0</td></tr>
<tr><td>Totales</td><td> 109 </td><td>109 </td><td>0</td></tr>

</table>



---
## ERRORES
En caso de `ERROR` la respuesta será en formato JSON de la siguiente forma:

```json
{
    'code': 400,
    'status': "Bad Request",
    'error': {
        "message": "(#400) Parameter 'vacantes' only accept boolean values."
        }
}
```
*Ejemplo de request `HTTP GET api/v2?sigla=DPT6100&vacantes=foo`*

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