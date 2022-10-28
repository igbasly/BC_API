"""
To automatically detect and add new routers and controllers, the file has to
have the following structure:

Name:
    The file name should be <NAME>_controller.py, where <NAME> is the
    controllers name.

Content:
    At least the base content for controllers shold be an instance of APIRouter
    at variable router.
    E.g.

    ```
        from fastapi import APIRouter

        router = APIRouter(tags=["<NAME>"])
    ```
    The router should include the tags attribute with the controller's name.

APIRouters works very similar to a FastAPI instances, you can easyly add new
routes with the decorator @router.<HTTP_METHOD>


NESTED CONTROLLERS:
    For nested controllers packages, you only have to add a folder named after
    your nested route. And then add new controllers inside them following the
    structure mentioned above.
    E.g.
    - controllers/
     |- __init__.py
     |
     |- api/
       |
       |- v1/
         |
         |- items_controllers.py

    This folder structure will generate `/api/v1/items` url.
    Where 'items_controllers` include all the necessary routes for items.


In case you want to add controllers with another structure, you have to add the
routes manually to the config/routes.py file.
"""
