from check_director import check_director
from check_owner import check_owner
import time, json

def owner_director(com_name_list, list_of_players, card_list, list_of_companies):
    for com in com_name_list:
        if com.company_total_buy_shares <= 100000:
            com.company_owner = check_owner(com, list_of_players)
            if com.company_owner:
                com.company_owner.player_connection.send(str.encode("RN"))
                ans = list(filter(lambda x: x.card_company == com.company_name, card_list))
                l1 = min(ans, key=lambda x: x.card_value,default=0)
                if l1:
                    least = min(l1.card_value,0)
                    for cards in ans:
                        com.company_owner.player_connection.send(json.dumps({cards.card_company: \
                            cards.card_value}).encode('utf-8'))
                        time.sleep(1)
                    com.company_owner.player_connection.send(str.encode("end"))
                    choice = com.company_owner.player_connection.recv(512).decode('utf-8').upper()
                    if choice == "Y":
                        com.company_current_price = max(list_of_companies[com.company_name] - least,0)

        if com.company_total_buy_shares <= 150000 and not com.company_owner:
            director = check_director(com, list_of_players)
            if director['fp']:
                director['fp'].player_connection.send(str.encode('dir,' + ','.join(director['players'])))
                time.sleep(1)
                choice = director['fp'].player_connection.recv(512).decode('utf-8').upper()
                if choice == "Y":
                    com.company_current_price = max(list_of_companies[com.company_name] - director['mv'],0)