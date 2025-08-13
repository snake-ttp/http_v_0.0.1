import socket
from Builder.responseBuilder import build_response
import threading

def parse_request(req_data):
    lines = req_data.split("\r\n")
    start_line = lines[0]
    method , path, version = start_line.split(" ")
    print("Method : " ,method)
    print("Path : ", path)
    print("Version: ", version)
    return method, path, version

def get_res(path):
    
    path_list: list = path.strip("/").split("/")
    
    if len(path_list) > 0 and path_list[0] == "echo":
        print(path)
        if len(path_list) >1:
            mesg = path_list[1]
            return build_response(mesg)
        else:
            return build_response("")
    elif len(path_list)>0 and path_list[0] == "user-agent":
        pass
            
    if path == "/":
        return build_response("<h1>hi welcome to HTTP server<h1> <h4>developd by Thush</h4>",content_type="text/html")
    
    return build_response("<h1>404 Not Found</h1>", status="404 Not Found", content_type="text/html")

def handle_request(client_socket: socket.socket):
    try:
        request_data = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break 
            request_data += data
            if b"\r\n\r\n" in request_data:
                break
        
        if request_data:
            m, p, v = parse_request(request_data.decode())
            res = get_res(p)
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
            # Create a new thread for each client connection
            client_handler = threading.Thread(target=handle_request, args=(client,))
            client_handler.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    main()
    
    
"""
    issue is port number 6000  change the port number 4123
"""