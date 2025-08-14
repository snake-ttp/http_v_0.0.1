import socket
from Builder.responseBuilder import build_response
import threading
import os

def parse_request(req_data):
    lines = req_data.split("\r\n")
    data_set = {}

    for x in lines[1:]:  # skip request line
        if ":" in x:
            key, value = x.split(":", 1)
            data_set[key.strip()] = value.strip()

    start_line = lines[0]
    method, path, version = start_line.split(" ")
    return method, path, version, data_set, ""

def get_res(path, data_set:dict, method: str ="GET",req_body:str = ""):
    
    path_list: list = path.strip("/").split("/")
    
    if method == "GET":
        if len(path_list) > 0 and path_list[0] == "echo":
            print(path)
            if len(path_list) >1:
                mesg = path_list[1]
                return build_response(mesg)
            else:
                return build_response("")
        elif len(path_list)>0 and path_list[0] == "user-agent":
            # check User-Agent header in data_set
            k = data_set.get("User-Agent")
            if k is not None:
                return build_response(k)
        elif len(path_list) > 0 and path_list[0] == "files":
            # generate file path
            path_arr: list = path_list[1:]
            if len(path_arr) > 1:
                file_path = "/".join(path_arr)
            else:
                file_path = path_list[1]
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path,"r") as f:
                        return build_response(f.read(),content_type="application/octet-stream")
                except:
                    return build_response(status="404 Not Found")
                    
            else:
                return build_response(status="404 Not Found")
            return build_response(file_path)
        
    if method == "POST":
        if len(path_list) > 0 and path_list[0] == "files":
            if len(path_list) >1 :
                path_arr: list = path_list[1:]
                if len(path_arr) > 1:
                    file_path = "/".join(path_arr)
                else:
                    file_path = path_list[1]
                with open(file_path, "w") as f:
                    f.write(req_body)
                return build_response(status="201 Created")
            else:
                return build_response("File cration Fail", status="400 Bad Request")
        
        
        
            
    if path == "/":
        return build_response("<h1>hi welcome to HTTP server<h1> <h4>developd by Thush</h4>",content_type="text/html")
    
    return build_response("<h1>404 Not Found</h1>", status="404 Not Found", content_type="text/html")

def handle_request(client_socket: socket.socket):
    try:
        # Step 1: Read until end of headers
        request_data = b""
        while b"\r\n\r\n" not in request_data:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            request_data += chunk

        # Step 2: Parse headers
        header_part, _, remaining = request_data.partition(b"\r\n\r\n")
        headers_text = header_part.decode()
        method, path, version, data_set, _ = parse_request(headers_text)

        # Step 3: Get content length
        content_length = int(data_set.get("Content-Length", 0))

        # Step 4: Read body
        body = remaining
        while len(body) < content_length:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            body += chunk

        # Step 5: Pass full body to handler
        res = get_res(path, data_set=data_set, method=method, req_body=body.decode())
        client_socket.sendall(res.encode())

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()


def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 4123), reuse_port=True)
    server_socket.listen()
    print("Server is running on port: 4123")
    
    while True:
        try:
            client, addr = server_socket.accept()
            print(f"Connection from {addr} has been established")
            # Create new thread for new client
            client_handler = threading.Thread(target=handle_request, args=(client,))
            # handle concurrent users 
            client_handler.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()
    
# Developed By Thush 
    
    
"""
    issue is port number 6000  change the port number 4123
"""