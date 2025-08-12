import socket

def parse_request(req_data):
    lines = req_data.split("\r\n")
    start_line = lines[0]
    method , path, version = start_line.split(" ")
    print("Method : " ,method)
    print("Path : ", path)
    print("Version: ", version)
    return method, path, version

def get_res(path):
    response: dict = {
        "/": "HTTP/1.1 200 OK\r\n\r\n"
    }
    path_list: list = path.strip("/").split("/")
    
    if len(path_list) > 0 and path_list[0] == "echo":
        print(path)
        if len(path_list) >1:
            mesg = path_list[1]
            l = len(mesg)
            response[f"/echo/{mesg}"] = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {l}\r\n\r\nabc"
        else:
            response[f"/echo"] = f"HTTP/1.1 200 )K\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    print(response)
    
    default_res = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response.get(path,default_res)

def handle_request(client_socket: socket.socket):
    data = client_socket.recv(1024)
    m ,p , v = parse_request(data.decode()) #method path version
    res = get_res(p)
    client_socket.send(res.encode())


def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 6000),reuse_port=True)
    #server_socket.accept() # wait for client
    print ("Server is running on port : 6000")
    
    #server_socket.listen()
    while True:
        try:
            client, addr = server_socket.accept()
            print(f"Connection from {addr} has been established")
            handle_request(client_socket=client)
            
            client.close()
            
        except Exception as e:
            print(f"Error {e}")
    
    


if __name__ == "__main__":
    main()
