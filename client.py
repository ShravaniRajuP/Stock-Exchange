import socket

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


def check_response(data):
    if data == 'host':
        host_file()
    else:
        non_hostfile()


Input = input('Enter Your Name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
check_response(Response.decode())
while True:
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()