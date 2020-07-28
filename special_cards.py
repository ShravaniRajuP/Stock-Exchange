from helper import print_name_amt_shares, broadcast, card_discard
from global_vars import get_clients

#Trade - Loan
def loan(current_player):
    clients = get_clients()
    current_player.player_amount += 100000
    print("{} {}".format(current_player.player_name,'loans'))
    broadcast(clients, current_player.player_name + ' loaned some money.')
    print_name_amt_shares(current_player)
    card_discard(current_player, 'Loan')
    
#Trade - Debenture
def debenture(current_player, company):
    clients = get_clients()
    if company.company_current_price == 0 and current_player.player_shares[company.company_name]:
        current_player.player_amount += \
            current_player.player_shares[company.company_name] * company.company_starting_price
        current_player.player_shares[company.company_name] = 0
        company.company_total_buy_shares += current_player.player_shares[company.company_name]
        print("{} {}".format(current_player.player_name,'debenture'))
        broadcast(clients, current_player.player_name + ' played debenture.')
        card_discard(current_player, 'Debenture')

#Trade - Rights
def rights(company, lp, name, cp):
    clients = get_clients()
    broadcast(clients, ', '.join([cp.player_name, " invoked rights in ", company.company_name]))
    for _ in range(len(lp)):
        available_shares = min((cp.player_shares[company.company_name]//2000) * \
            1000, company.company_total_buy_shares)
        check_amount = cp.player_amount - available_shares * 10
        if check_amount < 0:
            max_shares = (cp.player_amount//10000)
            cp.player_shares[company.company_name] = cp.player_shares[company.company_name] \
                + max_shares * 1000
            cp.player_amount -= max_shares * 10000
            company.company_total_buy_shares -= max_shares*1000
            print(cp.player_name,cp.player_amount,cp.player_shares)
        else:
            cp.player_shares[company.company_name] += available_shares
            cp.player_amount = check_amount
            company.company_total_buy_shares -= available_shares
        cp = lp[next(name)]
    card_discard(cp, 'Rights')
    return