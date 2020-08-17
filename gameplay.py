import time, json
from server import reset_server
from game import game
from owner_director import owner_director
from share_suspend import share_suspend_check
from helper import *
from global_vars import get_clients, get_host_name, get_loco, set_loco_first, get_cnl, set_loca_full, \
    get_loca, set_current_turn, get_current_turn, set_card_list_full, get_card_list, set_cnl_first, \
        set_ss_holder, get_ss_holder

def gamereplay():
    host_name = get_host_name()
    clients = get_clients()
    clients[host_name].send(str.encode('play again'))
    time.sleep(1)
    answer = clients[host_name].recv(512).decode('utf-8')
    if answer == 'Y' or answer == 'y':
        gameplay()
    elif answer == 'N' or answer == 'n':
        reset_server()
    else:
        gamereplay()

def gameplay():
    cards_first = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
    set_loco_first(cards_first)
    list_of_companies = get_loco()
    set_cnl_first()
    com_name_list = get_cnl()
    for com in com_name_list:
        com.company_current_price = com.company_starting_price
    set_loca_full(create_cards(list_of_companies))
    list_of_cards = get_loca()
    clients = get_clients()

    list_of_players = player_instance(clients)
    time.sleep(1)
    number_of_players = len(list_of_players)
    
    turn = 0
    rounds = 0
    set_card_list_full(assign_cards(list_of_cards, list_of_players))
    card_list = get_card_list()
    set_current_turn(round_robin(number_of_players))
    current_turn = get_current_turn()

    # ### Step Two: Start the game
    while rounds < 10:
        for player in list_of_players:
            player.player_connection.send(str.encode("Cards"))
            time.sleep(1)
            for cards in player.player_cards:
                if cards.card_company == 'Share Suspend':
                    set_ss_holder(player)
                player.player_connection.send(json.dumps({cards.card_company: cards.card_value}).encode('utf-8'))
                time.sleep(1)

        game(turn, 3 * number_of_players, list_of_players, current_turn)
        prev_list = list_of_companies.copy()
        for company in com_name_list:
            ans = filter(lambda x: x.card_company == company.company_name, card_list)
            final = sum(list(map(lambda x: x.card_value, list(ans))))
            company.company_current_price += final
            list_of_companies[company.company_name] += final
        
        ans_curr = filter(lambda x: x.card_company == 'Currency', card_list)
        final_curr = sum(list(map(lambda x: x.card_value, list(ans_curr))))
          
        for c in com_name_list:
            c.company_current_price = max(c.company_current_price, 0)
            
        print("\nEnd of Round {}\n".format(rounds+1))
        print(list(map(lambda x: {x.company_name:x.company_current_price},com_name_list)))

        broadcast_update()

        # Check Owner and Director for each company
        owner_director(com_name_list, list_of_players, card_list, list_of_companies)

        share_suspend_check(prev_list)

        broadcast_update()
        
        for c in com_name_list:
            list_of_companies[c.company_name] = c.company_current_price

        # Squaring off the short shares
        for all_player in list_of_players:
            for com,shares in all_player.player_shares.items():
                if shares < 0:
                    all_player.player_amount += (shares*prev_list[com]*-2) + \
                            ((prev_list[com] - list_of_companies[com])*shares*-1)
                    all_player.player_shares[com] = 0
            all_player.player_amount *= 1+(final_curr/100)
            all_player.player_amount = (all_player.player_amount // 1000)*1000

        # Resetting total short shares to maximum
        for com in com_name_list:
            com.company_total_sell_shares = 200000

        # Braodcasting player details 
        for player in list_of_players:
            print_name_amt_shares(player)

        time.sleep(1)
        turn = 0
        next(current_turn)
        set_card_list_full(assign_cards(list_of_cards, list_of_players))
        card_list = get_card_list()
        rounds += 1

    #Final calculation of each player  
    for all_player in list_of_players:
        for shares in all_player.player_shares.keys():
            all_player.player_amount += all_player.player_shares[shares] * list_of_companies[shares]
        broadcast(''.join(['Name: ',all_player.player_name,'; Amount: ',str(all_player.player_amount)]))
        time.sleep(1)
    
    gamereplay()