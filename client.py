import socket
import json
from Classes import Player, Cards, Company

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# Response = ClientSocket.recv(1024)
# print(Response.decode('utf-8'))

def host_file():
    Input = input("Number of players")
    ClientSocket.send(str.encode(Input))

def non_hostfile():
    print("Waiting for the host to start the game.")

def play():
    Input = input("Play your turn: ")
    ClientSocket.send(str.encode(Input))

def wait():
    pass

def check_response(data):
    # print(data)
    if data == 'host':
        host_file()
    elif data == 'play':
        play()
    elif data == 'wait':
        wait()
    # elif data == 'json':
    #     # b = b'' + ClientSocket.recv(1024)
    #     # Response = json.loads(b.decode('utf-8'))
    #     # Response = ClientSocket.recv(1024).decode('utf-8')
    #     print(Response)
    else:
        non_hostfile()
    return

Input = input('Enter Your Name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024).decode('utf-8')
print(Response)
check_response(Response)
while True:
    Response = ClientSocket.recv(1024).decode('utf-8')
    print(Response)
    check_response(Response)

ClientSocket.close()