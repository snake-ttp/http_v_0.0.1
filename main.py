import socket





def main():
    print("Hello from http-web-server!")
    server_socket = socket.create_server(("localhost", 8000),reuse_port=True)
    server_socket.accept() # wait for client


if __name__ == "__main__":
    main()
