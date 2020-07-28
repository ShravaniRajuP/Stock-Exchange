def check_owner(com, lp):
    for player in lp:
        if player.player_shares.get(com.company_name,0) >= 100000:
            return player
    return None