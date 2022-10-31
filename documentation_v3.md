# BuscaCursos UC REST API  | V3 | (_DEPRECATED_) 
REST API del sistema BuscaCursos de la PUC Chile.

La versión 3 de la API se encuentra alojada en la url [http://bc.horariomaker.com/api/v3](http://bc.horariomaker.com/api/v3)


## GET
---

### **Parametros**
```
GET /api/v3/parametros
```

Endpoint para obtener los parametros permitidos y vigentes de la API.

Response:
```json
{
    "code": 200,
    "data": {
        "parametros": {
            "semestre": [
            {
              "name": "2021 Segundo Semestre", 
              "value": "2021-2"
            }, 
            {
              "name": "2021 Primer Semestre", 
              "value": "2021-1"
            }, 
            {
              "name": "2020 TAV", 
              "value": "2020-3"
            }, 
            {
              "name": "2020 Segundo Semestre", 
              "value": "2020-2"
            }, 
            {
              "name": "2020 Primer Semestre", 
              "value": "2020-1"
            }
          ],
          "formato": [
            {
              "name": "-- Todos --", 
              "value": "TODOS"
            }, 
            {
              "name": "HIB - HÃ­brido", 
              "value": "HIB"
            }, 
            {
              "name": "OL - Remoto", 
              "value": "OL"
            }, 
            {
              "name": "PR - Presencial", 
              "value": "PR"
            }, 
            {
              "name": "REPR - Remoto con Act.Presencial", 
              "value": "REPR"
            }
          ],
          "campus": [...],
          "categoria": [...],
          "formacion_general": [...],
          "unidad_academica": [...],
        }
    }
}
```

### **Requests**

Es una API _read-only_ por lo que solo acepta el método HTTP GET con los siguientes parametros:
* semestre
    - 2020-1
    - 2020-2
    - 2020-3 (TAV verano 2021)
    - 2021-1
    - 2021-2
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
* requisitos
    - true
    - false


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
                "Vacantes totales":"31"
                },
            "Requisitos": {
                "Equivalencias": ["IRB1001"],
                "Prerequisitos": ["FIS1513","ICE1513","FIS1514","ICE1514"],
                "Relacion entre prerequisitos y restricciones": [],
                "Restricciones": []
               }
            }
        }
}
```
*Ejemplo de request `HTTP GET /api/v3?sigla=irb2001&requisitos=true`*

---

### **Requisitos**
El parametro `requisitos` recibe únicamente valores **booleanos** *(true o false)* donde la respuesta corresponde a un diccionario en la *keyword* **requisitos** para cada **curso** que se encuentre en la consulta.

```json
...
    'Requisitos': {
        "Equivalencias": ["MAT1523","MAT230E","MLM1130"],
        "Prerequisitos": [["MAT1202","MAT1512"],["MAT1202","MAT1620"],["MAT1203","MAT1512"],["MAT1203","MAT1620"]],
        "Relacion entre prerequisitos y restricciones": [],
        "Restricciones": []
    }
...
```
*Ejemplo correspondiente a los requisitos del curos `MAT1630`*

El detalle de esta respuesta se interpreta como:

<table>
<tr>
<th> </th>
<th> </th>
</tr>
<tr> <td>Equivalencias</td><td> MAT1523 o MAT230E o MLM1130</td></tr>
<tr><td>Prerequisitos </td><td> (MAT1202 Y MAT1512) o (MAT1202 y MAT1620) o (MAT1203 y MAT1512) o (MAT1203 y MAT1620)</td></tr>
<tr><td>Relacion entre prerequisitos y restricciones </td><td> No tiene</td></tr>
<tr><td>Restricciones </td><td> No tiene</td></tr>

</table>


Es decir, en caso de tener una **lista vacía** significa que el campo no contiene valores, en caso de **compartir la lista principal** son equivalentes y en caso de **compartir una sublista** estos (*de la sublista*) son todos requeridos y entre sublistas son equivalentes.

---
### **ERRORES**
En caso de `ERROR` la respuesta será en formato JSON de la siguiente forma:

* **Código de error:** 400 o 500
* **Status:** Estado general del *request*.
* **Error:** Contendrá la información respectiva a la consulta y el error generado.



```json
{
    "code":400,
    "status": "Bad Request",
    "error": {
        "invalid_arguments": ["formato", "vacantes"],
        "message": "(#400) Some arguments are not accepted."
        }
}
```
*Ejemplo de request `HTTP GET api/v1?sigla=iic2233&vacantes=true&formato=foo`*

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