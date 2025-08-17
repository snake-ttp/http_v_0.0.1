def build_response(content_encoding:bool , body: str="", status="200 OK", content_type="text/plain" ):
    response:str = f"HTTP/1.1 {status}\r\n"
    
    if content_type:
        response += (
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
        )
    if content_encoding:
        response += (
            f"Content-Encoding: gzip"
        )
    
    response += (
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )
    
    return response
    
    
    