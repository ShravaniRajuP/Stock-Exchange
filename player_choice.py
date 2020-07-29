import time
from helper import broadcast, print_name_amt_shares, card_check
from global_vars import get_clients, get_cnl, get_current_turn
from special_cards import loan, debenture, rights

list_of_players = None

def player_choice(current_player, lp):
    clients = get_clients()
    com_name_list = get_cnl()
    current_turn = get_current_turn()
    global list_of_players
    list_of_players = lp
    choice = current_player.player_connection.recv(1024).decode().split(',')
    try:
        if choice[0] in ['pass', '']:
            print("{} {}".format(current_player.player_name, choice[0]))
            broadcast(current_player.player_name + " passed.")
            time.sleep(1)
            return
        elif choice[0] in ['buy', 'sell', 'sbuy', 'ssell']:
            company = com_name_list[int(choice[1])-1]
            if choice[0] == 'buy':
                buy(clients, current_player, company, int(choice[2]))
            elif choice[0] == 'sell':
                sell(clients, current_player, company, int(choice[2]))
            elif choice[0] == 'ssell':
                ssell(clients, current_player,company,int(choice[2]))
            else:
                sbuy(clients, current_player,company,int(choice[2]))
            return
        elif choice[0] == 'loan' and card_check(current_player, choice[0]):
            loan(current_player)
        elif choice[0] == 'debenture' and card_check(current_player, choice[0]):
            company = com_name_list[int(choice[1])-1]
            debenture(current_player, company)
        elif choice[0] == 'rights' and card_check(current_player, choice[0]):
            company = com_name_list[int(choice[1])-1]
            print("Current player before rights  {}".format(current_player.player_name))
            rights(company, lp, current_turn, current_player)
            print("Current player after rights  {}".format(current_player.player_name))
            print("{} {}".format(current_player.player_name,choice))
            for player in lp:
                if player == current_player:
                    continue
                else:
                    print_name_amt_shares(player)
        return
    except Exception as e:
        print(str(e))
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,lp)

# Trade - Buy
def buy(clients, current_player, company, shares):
    if current_player.player_amount >= shares * company.company_current_price and \
            shares <= company.company_total_buy_shares:
        current_player.player_amount -= shares * company.company_current_price
        company.company_total_buy_shares -= shares
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) + shares                                                                                             
        broadcast(', '.join([current_player.player_name, "bought", company.company_name, str(shares)]))
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
def sell(clients, current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) >= shares:
        current_player.player_amount += shares*company.company_current_price
        company.company_total_buy_shares += shares
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) - shares
        broadcast(', '.join([current_player.player_name, "sold", company.company_name, str(shares)]))
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'sells'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to sell. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)

# Trade - Short Selling
def ssell(clients, current_player, company, shares):
    cost = shares*company.company_current_price*2
    if current_player.player_shares.get(company.company_name,0) <= 0 and \
        current_player.player_amount >= cost:
        current_player.player_amount -= cost
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) - shares
        company.company_total_sell_shares -= shares
        broadcast(', '.join([current_player.player_name, "shorts", company.company_name, str(shares)]))  
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'shorts'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to sell or not "\
            + "enough money. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)


# Trade - Short Buying
def sbuy(clients, current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) <= shares:
        current_player.player_shares[company.company_name] = \
            current_player.player_shares.get(company.company_name,0) + shares
        current_player.player_amount += shares*company.company_current_price*2
        company.company_total_sell_shares += shares
        broadcast(current_player.player_name + ',' + ','.join(["does not short sell ",\
            company.company_name, str(shares)]))
        print_name_amt_shares(current_player)
        print("{} {}".format(current_player.player_name,'buys short sold'))
    else:
        current_player.player_connection.send(str.encode("Not enough shares to buy. \n"))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        time.sleep(1)
        player_choice(current_player,list_of_players)