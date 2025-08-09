import socket

def parse_request(req_data):
    lines = req_data.split("\r\n")
    start_line = lines[0]
    method , path, version = start_line.split(" ")
    return method, path, version

def get_res(path):
    response = {
        "/": "HTTP/1.1 200 OK\r\n\r\n"
    }
    
    default_res = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response.get(path,default_res)

def handle_request(client_socket: socket.socket):
    client_socket.recv(1024)
    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response.encode())


def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 6000),reuse_port=True)
    #server_socket.accept() # wait for client
    print ("Server is running on port : 6000")
    
    #server_socket.listen()
    
    try:
        client, addr = server_socket.accept()
        print(f"Connection from {addr} has been established")
        handle_request(client_socket=client)
        
        client.close()
        
    except Exception as e:
        print(f"Error {e}")
    
    


if __name__ == "__main__":
    main()
