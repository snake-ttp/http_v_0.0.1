import socket

def handle_request(client_socket: socket.socket):
    client_socket.recv(1024)
    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response.encode())


def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 6000),reuse_port=True)
    #server_socket.accept() # wait for client
    print ("Server is running on port : 6000")
    
    server_socket.listen()
    try:
        client, addr = server_socket.accept()
        print(f"Connection from {addr} has been established")
        
    except Exception as e:
        print(f"Error {e}")
    
    


if __name__ == "__main__":
    main()
