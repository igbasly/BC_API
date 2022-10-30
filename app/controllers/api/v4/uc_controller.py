from fastapi import APIRouter, Request, Depends, Response, status


from app.models.uc.uc_parameter import UCSearchQuery, UCCourseInfoQuery
from app.responses import (
    UCResourcesResponse,
    UCParamsResponse,
    UCCoursesResponse,
    UCCourseResponse
)

from app.services import UCService


router = APIRouter(
    prefix="/uc",
    tags=["UC"]
)


@router.get('/', response_model=UCResourcesResponse)
def index(request: Request):
    """
    UC API index to get available endpoints.
    """
    base_url = request.url._url
    routes = list(map(
        lambda r: {
            "name": r.name,
            "url": f"{base_url}{r.path.replace('/uc/', '')}",
            "methods": r.methods,
        },
        router.routes
    ))

    return {"name": router.tags[0], "resources": routes, "url": base_url}


@router.get('/parameters', response_model=UCParamsResponse)
def parameters(request: Request):
    """
    To obtain available parameters for courses search.
    You will get an Array of Objects which represent every accepted parameter \
        in courses search. These objects have three attributes:
    * **name**: Is the parameter name to use in search.
    * **type**: Represent what kind of search field you are dealing with. It \
        could be:
        * _input_: a single string.
        * _select_: you can only search with one of the values included with \
            this parameter.
        * _datetime_: a string form of date with time in ISO format.
        * _boolean_: a string form of boolean value. For better understanding,\
             these values are included in the values section of the parameter.
    * **values**: _(optional)_ this attribute is only included with "select" \
        and "boolean" types of parameters. Represent an Array of Objects for \
            any possible value to use. Every object has the next structure:
        * _name_: represent the name of the  (for display propouses).
        * _value_: it is the specific value to be used.
    """
    service = UCService()
    params = service.authorized_params()

    return {"resources": params, "url": request.url._url}


@router.get('/{semester}/search', response_model=UCCoursesResponse)
def search_courses(
    request: Request,
    params: UCSearchQuery = Depends()
):
    """
    Search any course of BuscaCursos UC with the required parameters.
    """
    service = UCService()
    dict_params = params.sanitized_params()
    courses = service.search_courses(dict_params)

    return {"url": request.url._url, "resources": courses}


@router.get('/{semester}/{course_code}', response_model=UCCourseResponse)
def course_information(
    request: Request,
    response: Response,
    params: UCCourseInfoQuery = Depends()
):
    service = UCService()
    course_info = service.course_details(params.dict())

    if course_info:
        return {"url": request.url._url, "resource": course_info}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "url": request.url._url,
            "error": "Course information not found, please check semester "
                     "and course code"
        }
