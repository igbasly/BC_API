import requests
import json
from bs4 import BeautifulSoup

from app.assets import asset_path


def request_parameters():
    """Make the requests to BuscaCursos server and parse the xml response to
    separete all the parameters in a single object.
    Returns:
        dict: Object with all accepted paramters and its options values and
              names.
    """
    resp = requests.get("http://buscacursos.uc.cl/").text

    soup = BeautifulSoup(resp, "lxml")

    with open(asset_path('uc_params.json'), "r") as file_:
        params_names = json.load(file_)

    parameters = []

    for param in params_names:
        info = params_names[param]
        resource = {"name": param, "type": info[0]}
        if info[0] == "select":
            selects = soup.find_all("select", attrs={"name": info[1]})
            options = []
            if selects:
                select = selects[0]
                options_html = select.find_all("option")
                for op in options_html:
                    option = {"value": op["value"], "name": op.get_text()}
                    options.append(option)
            resource["values"] = options

        parameters.append(resource)

    return parameters
