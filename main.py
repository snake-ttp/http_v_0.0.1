import socket
from Builder.responseBuilder import build_response
import threading
import os
import gzip

def parse_request(req_data):
    lines = req_data.split("\r\n")
    data_set = {}

    for x in lines[1:]:  # skip request line
        if ":" in x:
            key, value = x.split(":", 1)
            data_set[key.strip()] = value.strip()

    start_line = lines[0]
    method, path, version = start_line.split(" ")
    print(method)
    print(path)
    print(version)
    return method, path, version, data_set, ""

def get_res(path, data_set:dict):
    
    path_list: list = path.strip("/").split("/")
    
    status: str = "200 OK"
    body: str = ""
    headers: dict = {"Content-Type": "text/plain"}
    
    if path == "/":   # root path
        body = "<h1>hi welcome to HTTP server<h1> <h4>developed by Thush</h4>"
        headers["Content-Type"] = "text/html"
    
    elif len(path_list) > 0 and path_list[0] == "echo":
        print(path)
        if len(path_list) >1:
            mesg = path_list[1]
            body = mesg
        else:
                body = mesg
    elif len(path_list)>0 and path_list[0] == "user-agent":
            # check User-Agent header in data_set
        k = data_set.get("User-Agent")
        if k is not None:
            #return build_response(k)
            body = k
        else:
            body = "No user-Agent found"
        headers["Content-Type"] = "text/plain"
        
    elif len(path_list) > 0 and path_list[0] == "files":
            # generate file path
        
        if len(path_list) > 1:
            file_path = "/".join(path_list[1:])
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path,"r") as f:
                        body = f.read()
                        headers["Content-Type"] = "application/octet-stream"
                        status = "200 OK"
                    
                except:
                    status = "500 Internal Server Error"
                    body = "<h1>Internal Server Error</h1>"
                    headers["Content-Type"] = "text/html"
            else:
                status = "404 Not Found"
                body = "<h1>Not Found :( <h1>"
                headers["Content-Type"] = "text/html"
        else:
            file_path = path_list[1]
            
        
                    
        # else:
        #     status = "404 Not Found"       
        body = file_path
        
    
    

    return status, body, headers
        
        
def post_res(path, data_set:dict, req_body:str):
    path_list: list = path.strip("/").split("/")
    status = "404 Not Found"
    body = "<h2>Not Found </h2>"
    headers: dict ={}
    if len(path_list) >1 :
        path_arr: list = path_list[1:]
        if len(path_arr) > 1:
            file_path = "/".join(path_arr)
        else:
            file_path = path_list[1]
            with open(file_path, "w") as f:
                f.write(req_body)
                status = "201 Created"
    else:
        body = "File cration Fail"
        status = "400 Bad Request"
    return status,body,headers
    
        

def handle_request(client_socket: socket.socket):
    try:
        # Step 1: Read until end of headers
        request_data = b""
        while b"\r\n\r\n" not in request_data:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            request_data += chunk
            
        header_part, _, remaining = request_data.partition(b"\r\n\r\n")
        headers_text = header_part.decode()
        method, path, version, data_set, _ = parse_request(headers_text)

        content_length = int(data_set.get("Content-Length", 0))

        #  Read body
        body = remaining
        while len(body) < content_length:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            body += chunk

        if method == "GET":
            s,b,h = get_res(path,data_set)
        elif method == "POST":
            s,b,h = post_res(path,data_set, body.decode())
        else:
            s = "405 Method Not Allowed"
            b = "<h1>405 Method Not Allowed</h1>"
            h = {}
            
        for x,y in data_set.items():
              
            if x == "Accept-Encoding":  # check heder is Accept-Encoding
                
                # y is string it contains values. like invalied-encode , gzip, invalied-encode
                # y string split , and added to list multiple elmnts
            
                l : list = [x.strip() for x in y.split(",")]
                if "gzip" in l:
                    h["Content-Encoding"] = "gzip" 
            
        
        res = build_response(b,s,h)
            
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
    
    try:
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
    except KeyboardInterrupt as e:
        print("Key Board Interupt")
    except Exception as e:
        print(f"err : {e}")
    finally:
        print("byeee!")

if __name__ == "__main__":
    main()
    
# Developed By Thush 
    
    
"""
    issue is port number 6000  change the port number 4123
"""