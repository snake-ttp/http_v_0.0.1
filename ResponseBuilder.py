import gzip

class ResponseBuilder:
    @staticmethod
    def build_response(body: str | bytes = "", status="200 OK", headers: dict = {}):
    
        if isinstance(body, str):
            raw_body = body.encode()
        else:
            raw_body = body

        if headers.get("Content-Encoding") == "gzip":  #chk gzip encoding
            raw_body = gzip.compress(raw_body)

        response = f"HTTP/1.1 {status}\r\n"
        response += f"Content-Length: {len(raw_body)}\r\n"

        if "Content-Type" in headers:
            response += f"Content-Type: {headers['Content-Type']}\r\n"
        if "Content-Encoding" in headers:
            response += f"Content-Encoding: {headers['Content-Encoding']}\r\n"

        response += "Connection: close\r\n\r\n"

        return response.encode() + raw_body