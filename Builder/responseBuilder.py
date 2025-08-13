def build_response(body: str="", status="200 OK", content_type="text/plain"):
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )