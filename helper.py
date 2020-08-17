
import random, time, json
from Classes import Cards, Player
from global_vars import get_clients, get_cnl
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

def print_name_amt_shares(current_player):
    current_player.player_connection.send(str.encode(''.join(['\nName: ', current_player.player_name,\
        '; Amount: ', str(current_player.player_amount), '; \nShares: '])))
    current_player.player_connection.send(json.dumps(current_player.player_shares).encode())
    time.sleep(1)

def assign_cards(list_cards, player_list):
    card_list = []
    for player in player_list:
        random.shuffle(list_cards)
        player.player_cards = sorted(list_cards[:10], key = lambda x: x.card_company)
        card_list += list_cards[:10]
        list_cards = list_cards[10:]
    return card_list

def round_robin(n):
    for i in range(1000):
        yield i % n

def player_instance(conns):
    lP = []
    for name, conn in conns.items():
        lP.append(Player(name, conn))
    return lP

#Check presence of respective card  
def card_check(current_player, choice):
    ans = list(filter(lambda x: x.card_company.lower().startswith(choice), current_player.player_cards))
    return len(ans)

def card_discard(current_player, choice):
    for idx,card in enumerate(current_player.player_cards):
        if card.card_company == choice:
            discard = idx
            current_player.player_cards.pop(discard)
            break

def broadcast(msg = None):
    clients = get_clients()
    for conn in clients.values():
        if type(msg) == str:
            conn.send(str.encode(msg))
        else:
            conn.send(json.dumps(msg).encode())

def broadcast_update():
    com_name_list = get_cnl()
    broadcast('update')
    time.sleep(1)
    for company in com_name_list:
        broadcast(str(company.company_current_price))
        time.sleep(1)

def squaring_short_shares(list_of_players, final_curr):
    for all_player in list_of_players:
        for com,shares in all_player.player_shares.items():
            if shares < 0:
                all_player.player_amount += (shares*prev_list[com]*-2) + \
                        ((prev_list[com] - list_of_companies[com])*shares*-1)
                all_player.player_shares[com] = 0
        all_player.player_amount *= 1+(final_curr/100)
        all_player.player_amount = (all_player.player_amount // 1000)*1000