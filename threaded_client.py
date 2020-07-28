from _thread import start_new_thread
from global_vars import get_clients, get_host_name

def threaded_client(connection, flag = 1, ):
    clients = get_clients()
    host_name = get_host_name()
    if flag: 
        player_name = connection.recv(2048).decode()
        print(player_name, " joined.")	
        clients[player_name] = connection
        print('Number of clients: ' + str(len(clients)))
        clients[host_name].send(str.encode(player_name + " joined."))