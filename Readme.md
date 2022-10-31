# BuscaCursos UC API :bookmark_tabs:

API REST para el sistema BuscaCursos de la Pontifica Universidad Católica de Chile.

Toda la documentación de las versiones, se puede encontrar en el sitio de [Documentación](http://igbasly.github.io/BC_API/).

## Versiones :books:

| Versión | Campos de búsqueda | Vacantes | Requisitos de cursos | Multiples cursos en una búsqueda |
|:---:|:---:|:---:| :---: | :---: |
V1 (deprecated) | :white_check_mark: | :x: | :x: | :x: |
V2 (deprecated) | :white_check_mark: | :white_check_mark: | :x: | :x: |
V3 (deprecated) | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: |
V4 (Actual) | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## Controladores :satellite:

Si quieres aportar y agregar un controlador, solo debes crear un archivo de nombre `<NAME>_controller.py`, donde `<NAME>` es el nombre que quieras darle a el controlador.

Este archivo debes ubiarlo en directorio `app/controllers` o en algún sub-directorio como `app/controllers/api/v4/` u otro que creas necesario agregar.

El nuevo controlador debe tener la estructura mencionada en `app/controllers/__init__.py`, de esta forma la aplicación lo reconocerá y agregará **automaticamente** a las rutas y documentación.

## Testing :test_tube:

Es importante que al hacer cualquier cambio en el repositorio, nos encarguemos de que los test vigentes sigan funcionando correctamente.

Además, cuando se agreguen nuevas funcionalidades se deben incluir con los tests correspondiente. Estos deben estar incluidos en el directorio `tests/` y siguiendo las convenciones de `pytest`.

Para ejecutar los test en el ambiente local, se debe estar dentro del repositorio y ejecutar:

```bash
 pytest --cov-config=.coveragerc --cov-report=term-missing --cov=app tests/
```
