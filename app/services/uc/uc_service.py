from app.services.uc.uc_scrappers import request_parameters
from app.services.base_service import BaseService
from app.models.uc import UCParameter


class UCService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def authorized_params(self):
        params = request_parameters()

        return list(map(lambda p: UCParameter(**p), params))
