from threaded_client import threaded_client
from _thread import start_new_thread
from helper import broadcast
import time
from gameplay import gameplay
from global_vars import get_serversocket, get_clients


def connections(num_of_players):
    ServerSocket = get_serversocket()
    count = 1
    clients = get_clients()
    while True:
        if count < num_of_players:
            Client, address = ServerSocket.accept()
            address
            count += 1
            start_new_thread(threaded_client, (Client,))
        else:
            if count == num_of_players and count == len(clients):
                num_of_players = 0
                broadcast(clients, ', '.join(clients.keys()))
                time.sleep(2)
                gameplay()
            else:
                continue