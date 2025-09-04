from typing import Tuple, Dict, List

class RequestParse:
    
    @staticmethod
    def parse(req_data: bytes) -> Tuple[str, str, str, Dict[str,str], bytes]:
        
        header ,_,body = req_data.partition(b"\r\n\r\n")
        
        header_txt = header.decode()
        lines = header_txt.split("\r\n")
        method, path, version = lines[0].split(" ")
        
        header_data_set = {}
        
        for l in lines[1:]:
            if ":" in l:
                key,value = l.split(":",1)
                header_data_set[key.strip()] = value.strip()
                
        return method, path, version,header_data_set, body
                