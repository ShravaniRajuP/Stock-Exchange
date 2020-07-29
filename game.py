import time
from player_choice import player_choice

def game(turn, num, list_of_players, current_turn): 
    while turn < num:
        current_player = list_of_players[next(current_turn)]
        for player in list_of_players:
            if player != current_player:
                player.player_connection.send(str.encode('wait ' + str(current_player.player_name)))
        time.sleep(1)
        current_player.player_connection.send(str.encode('play'))
        player_choice(current_player, list_of_players)
        print('End of turn {} \n'.format(turn+1))
        # print_name_amt_shares(current_player)
        turn += 1