from connections import connections
from threaded_client import threaded_client
from _thread import start_new_thread
from global_vars import get_serversocket, set_clients, set_host_name


def host_connections():
    ServerSocket = get_serversocket()
    print('Waiting for a host..')
    ServerSocket.listen(5) # error in replay - invalid argument, maybe related to binding. try
    Client, address = ServerSocket.accept()
    address
    host_name = Client.recv(1024).decode()
    set_host_name(host_name)
    print("Host Name: ",host_name)
    Client.send(str.encode('host'))
    num_of_players = int(Client.recv(1024).decode())
    print("Number of Players = ",str(num_of_players))
    set_clients(host_name, Client)
    start_new_thread(threaded_client, (Client, 0, ))
    connections(num_of_players)