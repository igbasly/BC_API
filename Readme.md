# BuscaCursos UC REST API
[![Build Status](https://travis-ci.com/igbasly/BC_API.svg?token=rvsCi5nQd3Zv6KdSdS54&branch=master)](https://travis-ci.com/igbasly/BC_API) [![Heroku](https://heroku-badge.herokuapp.com/?app=buscacursos-api&root=favicon.ico)]()

API REST para el sistema BuscaCursos de la Pontifica Universidad Católica de Chile.

Toda la documentación de las versiones, se puede encontrar en el sitio de [Documentación](http://igbasly.github.io/BC_API/).

## Versiones

| Versión | Campos de búsqueda | Vacantes | Requisitos de cursos |
|:---:|:---:|:---:| :---: |
V1| :white_check_mark: | :x: | :x: |
V2| :white_check_mark: | :white_check_mark: | :x: |
V3 (Actual)| :white_check_mark: | :white_check_mark: | :white_check_mark:

## Códigos de Error
| Código | Tipo de error | Descripción |
|:---:|:---:|:---|
|`200`| Ok| La consulta fue exitosa |
|`202`| Accepted | No se encontró información con los parametros dados. |
|`400`| Bad Request| Hay errores en la formulación de la consulta. |
|`405`| Method Not Allowed| Se utilizó un método HTTP no autorizado (`PUT`, `POST`, `PATCH`, `DELETE`) |
|`500`| Internal Server Error| Ha ocurrido un error en el servidor al manejar la consulta.|
|`503`| Service Unavailable| El servicio no se encuentra disponible momentaneamente. Probablemente sea por mantención.|
