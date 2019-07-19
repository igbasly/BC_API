# BuscaCursos UC REST API  | [![Build Status](https://travis-ci.com/igbasly/BC_API.svg?token=rvsCi5nQd3Zv6KdSdS54&branch=master)](https://travis-ci.com/igbasly/BC_API)
REST API del sistema BuscaCursos de la PUC Chile.\
La API se encuentra alojada en la url [buscacursos-api.herokuapp.com/api/v1](http://buscacursos-api.herokuapp.com/api/v1)


## GET
### Requests

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

Las respuesta son en formato JSON de la siguiente forma:
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


### ERRORS
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
