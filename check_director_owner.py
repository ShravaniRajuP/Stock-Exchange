def check_owner(com, lp):
    for player in lp:
        if player.player_shares.get(com.company_name, 0) >= 100000:
            return player
    return None

def check_director(com, lp):
    dir_list = {}
    dir_list['fp'] = None
    dir_list['mv'] = 0
    dir_list['players'] = []
    for player in lp:
        if player.player_shares.get(com.company_name, 0) >= 50000:
            if not dir_list['fp']:
                dir_list['fp'] = player
            dir_list['players'].append(player.player_name)
            ans = list(filter(lambda x: x.card_company == com.company_name, player.player_cards))
            l1 = min(ans, key = lambda x: x.card_value, default = 0)
            if l1:
                dir_list['mv'] = min(dir_list['mv'], l1.card_value)
    return dir_list