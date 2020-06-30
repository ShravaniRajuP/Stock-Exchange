import socket
import os
from _thread import start_new_thread
from Stock_Exchange import player_instance

ServerSocket = socket.socket()
host = ''
port = 1233
count = 1
clients = {}

try:
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))

def broadcast(conn_list, msg = None):
	for conn in conn_list.values():
		if msg:	
			conn.send(str.encode(msg))
		else:
			conn.send(str.encode(','.join(conn_list.keys())))

def threaded_client(connection, ):
	# connection.send(str.encode('Welcome..!! \n'))
	if len(clients)-1 >= 0: 
		player_name = connection.recv(2048).decode()
		print(player_name, " joined.")	
		clients[player_name] = Client
		print('Number of clients: ' + str(len(player_name)))
		clients[host_name].send(str.encode(player_name + " joined."))

def game():
	player_list = player_instance(clients)
	player_list[0].player_connection.send(str.encode('play'))
	

print('Waitiing for a host..')
ServerSocket.listen(5)
Client, address = ServerSocket.accept()
host_name = Client.recv(1024).decode()
print("Host Name: ",host_name)
Client.send(str.encode('host'))

num_of_players = int(Client.recv(1024).decode())
print("number of players = ",str(num_of_players))
clients[host_name] = Client
start_new_thread(threaded_client, (Client, ))

while True:
	if count < num_of_players:
		Client, address = ServerSocket.accept()
		count += 1
		start_new_thread(threaded_client, (Client, ))
	else:
		if count == num_of_players and count == len(clients):
			print("all Connected")
			num_of_players = 0
			broadcast(clients)
			# game starts
			game()
		else:
			continue