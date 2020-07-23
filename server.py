import socket, os, time, json, random
from _thread import start_new_thread
from Classes import Player, Cards, Company

# ### Step 0: Pre-game initializations
def create_cards(list_of_companies):
    price_range = [-30, -30, 30, 30, -25, -25, 25, 25, -20, -20, 20, 20,
                   -15, -15, 15, 15, -10, -10, 10, 10, -5, -5, 5, 5]
    list_cards, i, currency_range = [], 0, [-10, 10]
    company_range = [8, 12, 12, 16, 20, 24]
    special = ['Rights', 'Debenture', 'Loan', 'Share Suspend']

    # Company Shares
    for company in list_of_companies.keys():
        current_number = company_range[i]
        a = -current_number
        for value in price_range[a:]:
            temp = Cards(company, value)
            list_cards.append(temp)
        i += 1

    # Rights, Debenture, Loan, Share Suspend
    for i in range(7):
        list_cards.append(Cards(special[i // 2], 0))

    for i in currency_range:
        a = [Cards('Currency', i) for j in range(4)]
        list_cards += a
    return list_cards

def assign_cards(list_cards, player_list):
    for player in player_list:
        random.shuffle(list_cards)
        player.player_cards = sorted(list_cards[:10], key = lambda x: x.card_company)
        list_cards = list_cards[10:]

def player_instance(conns):
    lP = []
    for name, conn in conns.items():
        lP.append(Player(name, conn))
    return lP

def round_robin(n):
    for i in range(1000):
        yield i % n

def broadcast(clients, msg = None):
    for conn in clients.values():
        if type(msg) == str:
            conn.send(str.encode(msg))
        else:
            conn.send(json.dumps(msg).encode())

def print_name_amt_shares(current_player):
    current_player.player_connection.send(str.encode(''.join(['\nName: ', current_player.player_name,\
        '; Amount: ', str(current_player.player_amount), '; \nShares: '])))
    current_player.player_connection.send(json.dumps(current_player.player_shares).encode())
    time.sleep(1)

# Trade - Buy
def buy(current_player, company, shares):
    if current_player.player_amount >= shares * company.company_current_price and \
            shares <= company.company_total_buy_shares:
        current_player.player_amount -= shares * company.company_current_price
        company.company_total_buy_shares -= shares
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) + shares
        # if current_player.player_shares[company.company_name] >= 100000:
        #     company.company_owner.append(current_player)
        #     print("{} Owner: {}".format(company.company_name, current_player.player_name))
        # elif current_player.player_shares[company.company_name] >= 50000:
        #     company.company_director.append(current_player)
        #     print("{} Director: {}".format(company.company_name, current_player.player_name))                                                                                               
        broadcast(clients, ', '.join([current_player.player_name, "bought", company.company_name, str(shares)]))
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'buys'))
    else:
        current_player.player_connection.send(str.encode("Not enough money to"\
            " buy the shares or not enough shares available. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)
        
# Trade - Sell
def sell(current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) >= shares:
        current_player.player_amount += shares*company.company_current_price
        company.company_total_buy_shares += shares
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) - shares
        # if current_player in company.company_owner and current_player.player_shares[company.company_name] < 100000:
        #     company.company_owner.remove(current_player)
        #     print("{} not Owner: {}".format(company.company_name, current_player.player_name))
        # elif current_player in company.company_owner and current_player.player_shares[company.company_name] < 50000:
        #     company.company_director.remove(current_player)
        #     print("{} not director: {}".format(company.company_name, current_player.player_name))
        broadcast(clients, ', '.join([current_player.player_name, "sold", company.company_name, str(shares)]))
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'sells'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to sell. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)

# Trade - Short Selling
def ssell(current_player, company, shares):
    cost = shares*company.company_current_price*2
    if current_player.player_shares.get(company.company_name,0) <= 0 and \
        current_player.player_amount >= cost:
        current_player.player_amount -= cost
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) - shares
        company.company_total_sell_shares -= shares       
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'shorts'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to sell or not enough money. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)


# Trade - Short Buying
def sbuy(current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) <= shares:
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) + shares
        current_player.player_amount += shares*company.company_current_price*2
        company.company_total_sell_shares += shares
        broadcast(clients, current_player.player_name + ',' + ','.join(["does not short sell ",\
            company.company_name, str(shares)]))
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'buys short sold'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to buy. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)

#Check presence of respective card  
def card_check(current_player, choice):
    ans = list(filter(lambda x: x.card_company.lower().startswith(choice), current_player.player_cards))
    return len(ans)

#Trade - Loan
def loan(current_player):
    current_player.player_amount += 100000
    for idx,card in enumerate(current_player.player_cards):
        if card.card_company == 'Loan':
            discard = idx
            print("{} {}".format(current_player.player_name,'loans'))
    current_player.player_cards.pop(discard)
    
#Trade - Debenture
def debenture(current_player, company):
    if company.company_current_price == 0 and current_player.player_shares[company.company_name]:
        current_player.player_amount += \
            current_player.player_shares[company.company_name] * company.company_starting_price
        current_player.player_shares[company.company_name] = 0
        company.company_total_buy_shares += current_player.player_shares[company.company_name]
        print("{} {}".format(current_player.player_name,'debenture'))

#Trade - Rights
def rights(company, lp):
    for name in lp:
        available_shares = min((name.player_shares[company.company_name]//2000) * \
            1000, company.company_total_buy_shares)
        check_amount = name.player_amount - available_shares * 10
        if check_amount < 0:
            max_shares = (name.player_amount//10000)
            name.player_shares[company.company_name] = name.player_shares[company.company_name] \
                + max_shares * 1000
            name.player_amount -= max_shares * 10000
            company.company_total_buy_shares -= max_shares*1000
            print(name.player_name,name.player_amount,name.player_shares)
        else:
            name.player_shares[company.company_name] += available_shares*1000
            name.player_amount = check_amount
            company.company_total_buy_shares -= available_shares
    return

# Check Owner
def check_owner(com, lp):
    for player in lp:
        if player.player_shares.get(com.company_name,0) >= 100000:
            return player

#Check Director
def check_director(com, lp):
    dir_list = []
    for player in lp:
        if player.player_shares.get(com.company_name,0) >= 50000:
            dir_list.append(player)
    return dir_list

#Round - Share Suspend
def share_suspend(cp, prev_list):
    choice = cp.recv(512).decode('utf-8')
    if choice != str(0):
        print(choice)
        company = com_name_list[int(choice) - 1]
        company.company_current_price = prev_list[company.company_name]
        global list_of_companies
        list_of_companies[company.company_name] = prev_list[company.company_name]
        return 1
    else:
        return 0

def share_suspend_check(prev_list):
    # share_suspend()
    global share_suspend_holder
    if share_suspend_holder:
        share_suspend_holder.player_connection.send(str.encode('suspend'))
        time.sleep(1)
        if share_suspend(share_suspend_holder.player_connection, prev_list):
            broadcast(clients, 'update')
            time.sleep(1)
            for company in com_name_list:
                broadcast(clients, str(company.company_current_price))
                time.sleep(1)
        share_suspend_holder = None

# Pass / Buy / Sell (?)
def player_choice(current_player,lp):
    choice = current_player.player_connection.recv(1024).decode().split(',')
    # try:
    if choice[0] in ['pass', '']:
        print("{} {}".format(current_player.player_name,choice))
        broadcast(clients, "Passed.")
        time.sleep(1)
        return
    elif choice[0] in ['buy', 'sell', 'sbuy', 'ssell']:
        company = com_name_list[int(choice[1])-1]
        if choice[0] == 'buy':
            buy(current_player, company, int(choice[2]))
        elif choice[0] == 'sell':
            sell(current_player, company, int(choice[2]))
        elif choice[0] == 'ssell':
            ssell(current_player,company,int(choice[2]))
        else:
            sbuy(current_player,company,int(choice[2]))
        return
    elif choice[0] == 'loan' and card_check(current_player, choice[0]):
        loan(current_player)
    elif choice[0] == 'debenture' and card_check(current_player, choice[0]):
        company = com_name_list[int(choice[1])-1]
        debenture(current_player, company)
    elif choice[0] == 'rights' and card_check(current_player, choice[0]):
        company = com_name_list[int(choice[1])-1]
        rights(company,lp)
        print("{} {}".format(current_player.player_name,choice))
        for player in lp:
            if player == current_player:
                continue
            else:
                print_name_amt_shares(player)
    return
    # except:
    #     print('try-except')
    #     current_player.player_connection.send(str.encode('play'))
    #     time.sleep(1)
    #     player_choice(current_player,lp)

# Game begins
def game(turn,num, list_of_players): 
    while turn < num:
        current_player = list_of_players[next(current_turn)]
        if turn < len(list_of_players):
            current_player.player_connection.send(str.encode("Cards"))
            time.sleep(1)
            for cards in current_player.player_cards:
                if cards.card_company == 'Share Suspend':
                    global share_suspend_holder
                    share_suspend_holder = current_player
                current_player.player_connection.send(json.dumps({cards.card_company: cards.card_value}).encode('utf-8'))
                time.sleep(1)
        for player in list_of_players:
            if player != current_player:
                player.player_connection.send(str.encode('wait ' + str(current_player.player_name)))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        
        ## Trade
        player_choice(current_player,list_of_players)
        
        #End Turn 
        print('End of turn {} \n'.format(turn+1))
        # print_name_amt_shares(current_player)
        turn += 1

def reset_game():
    global list_of_companies
    list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
    for com in com_name_list:
        com.company_current_price = com.company_starting_price

def game_replay():
    clients[host_name].send(str.encode('play again'))
    time.sleep(1)
    answer = clients[host_name].recv(512).decode('utf-8')
    if answer == 'Y' or answer == 'y':
        reset_game()
        gameplay()
    elif answer == 'N' or answer == 'n':
        server()
    else:
        game_replay()

def gameplay():
    list_of_players = player_instance(clients)
    time.sleep(1)
    number_of_players = len(list_of_players)
    
    turn = 0
    rounds = 0
    assign_cards(list_of_cards,list_of_players)
    global current_turn
    current_turn = round_robin(number_of_players)

    # ### Step Two: Start the game
    while rounds < 2:
        game(turn, 3 * number_of_players, list_of_players)
        final_curr = 0
        prev_list = list_of_companies.copy()
                
        for cp in list_of_players:
            for idx, com in enumerate(list_of_companies.keys()):
                ans = filter(lambda x: x.card_company == com, cp.player_cards)
                final = sum(list(map(lambda x: x.card_value, list(ans))))
                com_name_list[idx].company_current_price += final
                list_of_companies[com] += final
            ans_curr = filter(lambda x: x.card_company == 'Currency', cp.player_cards)
            final_curr += sum(list(map(lambda x: x.card_value, list(ans_curr))))       
        
        for c in com_name_list:
            c.company_current_price = max(c.company_current_price, 0)
            
        print("\nEnd of Round {}\n".format(rounds+1))
        print(list(map(lambda x: {x.company_name:x.company_current_price},com_name_list)))

        broadcast(clients, 'update')
        for company in com_name_list:
            broadcast(clients, str(company.company_current_price))
            time.sleep(1)

        owner = None
        for com in com_name_list:
            if com.company_total_buy_shares < 100000:
                owner = check_owner(com, list_of_players)
                if owner:
                    least = [min(x.player_shares.values()) for x in list_of_players]
                    owner.player_connection.send(str.encode("RN"))
                    time.sleep(1)
                    ans = owner[0].player_connection.recv(512).decode('utf-8')
            elif com.company_total_buy_shares < 150000:
                director = check_director(com,list_of_players)

        if owner:
            owner.player_connection.send(str.encode("RN"))
            time.sleep(1)
            ans = owner[0].player_connection.recv(512).decode('utf-8')

        share_suspend_check(prev_list)

        # Squaring off the short shares
        for all_player in list_of_players:
            for com,shares in all_player.player_shares.items():
                if shares < 0:
                    all_player.player_amount += (shares*prev_list[com]*-2) + \
                                                ((prev_list[com] - list_of_companies[com])*shares*-1)
                    all_player.player_shares[com] = 0
            all_player.player_amount *= (1+final_curr/100)

        # Resetting total short shares to maximum
        for com in com_name_list:
            com.company_total_sell_shares = 200000

        # Braodcasting player details 
        for player in list_of_players:
            print_name_amt_shares(player)

        time.sleep(1)
        turn = 0
        next(current_turn)
        assign_cards(list_of_cards,list_of_players)
        rounds += 1

    #Final calculation of each player  
    for all_player in list_of_players:
        for shares in all_player.player_shares.keys():
            all_player.player_amount += all_player.player_shares[shares] * list_of_companies[shares]
        broadcast(clients,' '.join(['Name: ',all_player.player_name,'; Amount: ',str(all_player.player_amount)]))
        time.sleep(1)
        game_replay()

ServerSocket = socket.socket()
host, port, clients, list_of_players, host_name = '', 1233, {}, [], None
count, current_turn, share_suspend_holder = 1, None, None
list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]
list_of_cards = create_cards(list_of_companies)

def threaded_client(connection, flag = 1, ):
    if flag: 
        player_name = connection.recv(2048).decode()
        print(player_name, " joined.")	
        clients[player_name] = connection
        print('Number of clients: ' + str(len(clients)))
        clients[host_name].send(str.encode(player_name + " joined."))

def connections(num_of_players):
    while True:
        global count
        if count < num_of_players:
            Client, address = ServerSocket.accept()
            count += 1
            start_new_thread(threaded_client, (Client, ))
        else:
            if count == num_of_players and count == len(clients):
                num_of_players = 0
                broadcast(clients, ', '.join(clients.keys()))
                time.sleep(2)
                gameplay()
            else:
                continue

def host_connections():
    print('Waiting for a host..')
    ServerSocket.listen(5)
    Client, address = ServerSocket.accept()
    global host_name
    host_name = Client.recv(1024).decode()
    print("Host Name: ",host_name)
    Client.send(str.encode('host'))
    num_of_players = int(Client.recv(1024).decode())
    print("Number of Players = ",str(num_of_players))
    clients[host_name] = Client
    start_new_thread(threaded_client, (Client, 0, ))
    connections(num_of_players)

def server():
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    ip = socket.gethostbyname(socket.gethostname())
    print("IP address for connection : ")
    print(ip)
    host_connections()
    
if __name__ == "__main__":
    server()