from broadcast import broadcast
from print import print_name_amt_shares

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

