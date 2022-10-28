from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    def authorized_params(self):
        pass  # pragma: no cover
