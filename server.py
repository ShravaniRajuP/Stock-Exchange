import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = ''
port = 1233
all_connections = []
nameOfClients = []
game = 0

try:
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))



def broadcast(conn_list):
	for conn in conn_list:
		conn.sendall(str.encode(','.join(nameOfClients)))



def threaded_client(connection):
	connection.send(str.encode('Welcome..!! \n'))
	if len(nameOfClients[1:]) >= 0: 
		player_name = connection.recv(2048).decode()
		print(player_name, " joined.")
		nameOfClients.append(player_name)
		print('Number of clients: ' + str(len(nameOfClients)))
		all_connections[0].send(str.encode(player_name + " joined."))

print('Waitiing for a host..')
ServerSocket.listen(5)
Client, address = ServerSocket.accept()
host_name = Client.recv(1024).decode()
print("Host Name: ",host_name)
Client.send(str.encode('host'))

num_of_players = int(Client.recv(1024).decode())
print("number of players = ",str(num_of_players))
all_connections.append(Client)
nameOfClients.append(host_name)
start_new_thread(threaded_client, (Client, ))

while True:
	if len(all_connections) < num_of_players:
		print(len(all_connections))
		Client, address = ServerSocket.accept()
		all_connections.append(Client)
		start_new_thread(threaded_client, (Client, ))
	else:
		if len(all_connections) == num_of_players and len(all_connections) == len(nameOfClients):
			print("all Connected")
			broadcast(all_connections)
			num_of_players = 0
		else:
			continue