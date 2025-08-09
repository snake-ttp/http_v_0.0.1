import socket


def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 8000),reuse_port=True)
    #server_socket.accept() # wait for client
    
    server_socket.listen()
    
    client, addr = server_socket.accept()
    client.sendall("HTTP/1.1 200 OK\r\n\r\n".encode("utf-8"))
    


if __name__ == "__main__":
    main()
