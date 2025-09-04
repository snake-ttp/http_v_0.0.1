from abc import abstractmethod, ABC
from typing import Dict, Tuple, List

class RouteHandler(ABC):
    @abstractmethod
    def handle(self, path: str, header: Dict[str,str], body: bytes) -> Tuple[str,bytes, Dict[str,str]]:
        pass
    
    
    
class RootHandler(RouteHandler):
    def handle(self, path, header, body)-> Tuple[str,bytes, Dict[str,str]]:
        
        return path, header, body