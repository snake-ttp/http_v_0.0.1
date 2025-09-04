from abc import abstractmethod, ABC
from typing import Dict

class RouteHandler:
    @staticmethod
    def handle(self, path: str, header: Dict[str,str], body: bytes):
        pass