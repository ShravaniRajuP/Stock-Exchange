import socket
import os
from _thread import start_new_thread
import time
import json
from Classes import Player

ServerSocket = socket.socket()
host = ''
port = 1233
count = 1
clients = {}

def broadcast(clients, msg = None):
	print("broadcast")
	print(clients)
	for conn in clients.values():
		if msg:	
			conn.send(str.encode(msg))
		else:
			conn.send(str.encode(', '.join(clients.keys())))

def threaded_client(connection, flag = 1, ):
	# connection.send(str.encode('Welcome..!! \n'))
	if flag: 
		player_name = connection.recv(2048).decode()
		print(player_name, " joined.")	
		clients[player_name] = Client
		print('Number of clients: ' + str(len(player_name)))
		clients[host_name].send(str.encode(player_name + " joined."))

def game_():
	player_list = player_instance(clients)
	current_turn = round_robin(len(player_list))

	player_list[0].player_connection.send(str.encode('play'))
	time.sleep(5)
	print()
	# player_list[0].player_connection.send(str.encode('json'))
	player_list[0].player_connection.send(json.dumps({1: 'a', 2: 'b'}).encode('utf-8'))
	# broadcast("Server")
	gameplay(player_list)

if __name__ == "__main__":	
	
	from Stock_Exchange import player_instance, gameplay, round_robin	
	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waitiing for a host..')
	ServerSocket.listen(5)
	Client, address = ServerSocket.accept()
	host_name = Client.recv(1024).decode()
	print("Host Name: ",host_name)
	Client.send(str.encode('host'))

	num_of_players = int(Client.recv(1024).decode())
	print("number of players = ",str(num_of_players))
	clients[host_name] = Client
	start_new_thread(threaded_client, (Client, 0, ))

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
				time.sleep(5)
				# game starts
				game_()
			else:
				continue