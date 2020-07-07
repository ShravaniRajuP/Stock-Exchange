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

# ### Step 0: Pre-game initializations

from Classes import Player, Cards, Company

import random
import time

def create_company(list_of_companies):
    price_range = [-30, -30, 30, 30, -25, -25, 25, 25, -20, -20, 20, 20,
                   -15, -15, 15, 15, -10, -10, 10, 10, -5, -5, 5, 5]
    list_cards = []
    company_range = [8, 12, 12, 16, 20, 24]
    i = 0
    for company in list_of_companies.keys():
        current_number = company_range[i]
        a = -current_number
        for value in price_range[a:]:
            temp = Cards(company, value)
            list_cards.append(temp)
        i += 1
    return list_cards

def assign_cards(list_cards, player_list):
    for player in player_list:
        random.shuffle(list_cards)
        player.player_cards = sorted(list_cards[:10],key=lambda x: x.card_company)
        list_cards = list_cards[10:]

def player_instance(conns):
    list_of_players = []
    for name, conn in conns.items():
        list_of_players.append(Player(name, conn))
    return list_of_players

def round_robin(n):
    for i in range(1000):
        yield i%n


# Print player information before and after playing turn
def print_trade(current_player, c = '', company = None, shares = 0, choice = 0):
    pass

# Trade - Buy
def buy(current_player, company, shares):
    if current_player.player_amount >= shares * company.company_current_price:
        current_player.player_amount -= shares * company.company_current_price
        current_player.player_shares[company.company_name] = current_player.player_shares.get(company.company_name,0) + shares
    else:
        current_player.player_connection.send(str.encode("Not enough money to buy the shares \n"))
        player_choice(current_player)
        
# Trade - Sell
def sell(current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) >= shares:
        current_player.player_amount += shares*company.company_current_price
        current_player.player_shares[company.company_name] = current_player.player_shares.get(company.company_name,0) - shares
    else:
        current_player.player_connection.send(str.encode("Not enough shares to sell. \n"))
        player_choice(current_player)

# def check(company_name,current_player=None,choice=None):
    
    
# Pass / Buy / Sell (?)
def player_choice(current_player):
    choice = current_player.player_connection.recv(1024).decode().split(',')
    print(choice)
    
    if choice[0] == 'pass' or choice[0] == '':
        print("{} {}".format(current_player.player_name,choice))
        return
    elif choice[0] == 'buy' or choice[0] == 'sell':
        company = com_name_list[int(choice[1])-1] 
        print(company)
        if choice[0] == 'buy':
            buy(current_player, company, int(choice[2]))
        else:
            sell(current_player, company, int(choice[2]))
        print("{} {}".format(current_player.player_name,choice))
        broadcast(clients, current_player.player_name + ',' + ','.join(choice))
    return
    #     print_trade(current_player, company, 'after', shares, choice)

# Game begins
def game(turn,num, list_of_players): 
    while turn < num:
        current_player = list_of_players[next(current_turn)]    
        print_trade(current_player)
        current_player.player_connection.send(str.encode("Cards"))
        for cards in current_player.player_cards:
            current_player.player_connection.send(json.dumps({cards.card_company: cards.card_value}).encode('utf-8'))
            time.sleep(1)
        time.sleep(2)
        current_player.player_connection.send(str.encode('play'))
        ## Trade
        player_choice(current_player)
        
        #End Turn 
        print('\nEnd of turn {}'.format(turn+1))
        time.sleep(2)
        turn += 1

def broadcast(clients, msg = None):
    for conn in clients.values():
        if type(msg) == str:
            conn.send(str.encode(msg))
        else:
            conn.send(json.dumps(msg).encode())

def threaded_client(connection, flag = 1, ):
	# connection.send(str.encode('Welcome..!! \n'))
	if flag: 
		player_name = connection.recv(2048).decode()
		print(player_name, " joined.")	
		clients[player_name] = Client
		print('Number of clients: ' + str(len(player_name)))
		clients[host_name].send(str.encode(player_name + " joined."))

# ### Step One: Create Players and List of Cards and Initialize
list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]
list_of_cards = create_company(list_of_companies)
list_of_players = []
current_turn = None

def gameplay():
    list_of_players = player_instance(clients)
    time.sleep(3)
    number_of_players = len(list_of_players)
    
	# player_list[0].player_connection.send(json.dumps({1: 'a', 2: 'b'}).encode('utf-8'))
    # Redundant - Done in client
    # for player in list_of_players:
    # #     print(player.player_name,player.player_amount)
    #     broadcast(clients, ': '.join([player.player_name, str(player.player_amount)]))
    #     broadcast(clients, player.player_shares)
    
    turn = 0
    rounds = 0
    assign_cards(list_of_cards,list_of_players)
    global current_turn
    current_turn = round_robin(number_of_players)

    # ### Step Two: Start the game
    while rounds < 5:
        game(turn,2*number_of_players, list_of_players)
        for cp in list_of_players:
            for idx,com in enumerate(list_of_companies.keys()):
                ans = filter(lambda x: x.card_company == com,cp.player_cards)
                final = sum(list(map(lambda x: x.card_value, list(ans))))
                com_name_list[idx].company_current_price += final
                
        for c in com_name_list:
            c.company_current_price = max(c.company_current_price, 0)
            
        
        print("\nEnd of Round {}\n".format(rounds+1))
        print(list(map(lambda x: {x.company_name:x.company_current_price},com_name_list)))
        broadcast(clients, 'update')
        for company in com_name_list:
            broadcast(clients, str(company.company_current_price))
            time.sleep(1)

        for player in list_of_players:
            broadcast(clients,' '.join(['Name: ',player.player_name,'; Amount: ',str(player.player_amount), '; \nShares: ']))
            broadcast(clients,player.player_shares)
            time.sleep(1)

        time.sleep(3)
        turn = 0
        next(current_turn)
        assign_cards(list_of_cards,list_of_players)
        rounds += 1
        
    for current_player in list_of_players:
        for shares in current_player.player_shares.keys():
            current_player.player_amount += current_player.player_shares[shares] * list_of_companies[shares]

        broadcast(clients,' '.join(['Name: ',player.player_name,'; Amount: ',str(player.player_amount)]))
            
    # for current_player in list_of_players:
    #     print("Name : {} \t Amount : {}".format(current_player.player_name,current_player.player_amount))
    #     print("Current Shares : {}".format(current_player.player_shares))

if __name__ == "__main__":
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
    print("Number of Players = ",str(num_of_players))
    clients[host_name] = Client
    start_new_thread(threaded_client, (Client, 0, ))

    while True:
        if count < num_of_players:
            Client, address = ServerSocket.accept()
            count += 1
            start_new_thread(threaded_client, (Client, ))
        else:
            if count == num_of_players and count == len(clients):
                num_of_players = 0
                broadcast(clients, ','.join(clients.keys()))
                time.sleep(3)
                gameplay()
            else:
                continue