def build_response(body: str="", status="200 OK", headers: dict = {}):
    response:str = f"HTTP/1.1 {status}\r\n"
    
    for x,y in headers.items():
        if x == "Content-Type":
            response += (
                f"Content-Type: {y}\r\n"
                f"Content-Length: {len(body.encode())}\r\n"
            )
            continue
        response += (
            f"{x}: {y}\r\n"
        )
    
    response += (
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )
    
    return response

#print(build_response("asasdas","200 OK",{"Content-Type":"text/html","Content-Encoding":"gzip"}))
    
    
    