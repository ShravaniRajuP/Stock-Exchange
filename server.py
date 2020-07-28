import socket, os, time, json, random
from global_vars import set_serversocket, get_serversocket,\
     set_host_port, get_host_port

def server():
    from host_connection import host_connections
    set_serversocket()
    ServerSocket = get_serversocket()
    set_host_port('', 1233)
    try:
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ServerSocket.bind((get_host_port()))
    except socket.error as e:
        print(str(e))
    ip = socket.gethostbyname(socket.gethostname())
    print("IP address for connection: ", ip)
    host_connections()

def reset_server():
    ServerSocket = get_serversocket()
    ServerSocket.close()
    server()
    
if __name__ == "__main__":
    server()