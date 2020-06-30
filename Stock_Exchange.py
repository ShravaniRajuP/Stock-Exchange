#!/usr/bin/env python
# coding: utf-8

# ### Step 0: Pre-game initializations

# In[2]:

# from server import broadcast
from Classes import Player, Cards, Company

# In[ ]:
import random
import time

def create_company(list_of_companies):
    price_range = [-30, -30, 30, 30, -25, -25, 25, 25, -20, -20, 20, 20,
                   -15, -15, 15, 15, -10, -10, 10, 10, -5, -5, 5, 5]
    list_cards = []
    company_range = [8, 12, 12, 16, 20, 24]
    i = 0
    for company in list_of_companies.keys():
        current_number = company_range[i]
        a = -current_number
        for value in price_range[a:]:
            temp = Cards(company, value)
            list_cards.append(temp)
        i += 1
    return list_cards

def assign_cards(list_cards, player_list):
    for player in player_list:
        random.shuffle(list_cards)
        player.player_cards = sorted(list_cards[:10],key=lambda x: x.card_company)
        list_cards = list_cards[10:]

def player_instance(conns):
    list_of_players = []
    for name, conn in conns.items():
        list_of_players.append(Player(name, conn))
    return list_of_players

def round_robin(n):
    for i in range(1000):
        yield i%n


# In[ ]:


# Print player information before and after playing turn
def print_trade(current_player, c = '', company = None, shares = 0, choice = 0):
    pass
    # broadcast({'Name': current_player.)
    # if c == 'after':
    #     ### Print After Trade
    #     print("\n{}, {}, {}, {}".format(current_player.player_name,choice,shares,company.company_name))
    # ### Print Before & After Trade
    # print("\nName : {} \t Amount : {}".format(current_player.player_name,current_player.player_amount))
    # print("Current Shares : {}".format(current_player.player_shares))
    
# Trade - Buy
def buy(current_player, company, shares):
    if current_player.player_amount >= shares * company.company_current_price:
        current_player.player_amount -= shares * company.company_current_price
        current_player.player_shares[company.company_name] = current_player.player_shares.get(company.company_name,0) + shares
    else:
        print("Not enough money to buy the shares \n")
        player_choice(current_player)
        
# Trade - Sell
def sell(current_player, company, shares):
    if current_player.player_shares.get(company.company_name,0) >= shares:
        current_player.player_amount += shares*company.company_current_price
        current_player.player_shares[company.company_name] = current_player.player_shares.get(company.company_name,0) - shares
    else:
        print("Not enough shares to sell. \n")
        player_choice(current_player)

# def check(company_name,current_player=None,choice=None):
    
    
# Pass / Buy / Sell (?)
def player_choice(current_player):
    choice = input("\nEnter your choice(buy/sell/pass): ")
    if choice == 'pass' or choice == '':
        print("{} {}".format(current_player.player_name,choice))
        return
    elif choice == 'buy' or choice == 'sell':
        print("\n")
        print(list(map(lambda x: x.company_name,com_name_list)))
        com_num = int(input("Enter the company number: "))
        company = com_name_list[com_num-1] 
        shares = int(input("Enter the number of shares: "))
        if choice == 'buy':
            buy(current_player, company, shares)
        else:
            sell(current_player, company, shares)
        print_trade(current_player, company, 'after', shares, choice)
    else:
        player_choice(current_player)

# Game begins
def game(turn,num, list_of_players): 
    while turn < num:
        current_player = list_of_players[next(current_turn)]    
        print_trade(current_player)
        print("Cards: ")
        for cards in current_player.player_cards:
            print("\t{}: {}".format(cards.card_company, cards.card_value))
        print("\nPrice List: ", end="")
        print(list(map(lambda x: {x.company_name: x.company_current_price},com_name_list)))

        ## Trade
        player_choice(current_player)

        #End Turn 
        print('\nEnd of turn {}'.format(turn+1))
        time.sleep(2)
        turn += 1
#         except:
#             player_choice(current_player)
#             print('\nEnd of turn {}'.format(turn+1))
#             time.sleep(5)
#             turn += 1


# ### Step One: Create Players and List of Cards and Initialize

# In[ ]:

list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]
list_of_cards = create_company(list_of_companies)
list_of_players = []
current_turn = None

def gameplay(player_list):
    print("Gameplay")
    list_of_players = player_list
    number_of_players = len(list_of_players)
    for player in list_of_players:
        print(player.player_name,player.player_amount)
    
    turn = 0
    rounds = 0
    assign_cards(list_of_cards,list_of_players)
    global current_turn
    current_turn = round_robin(number_of_players)

    # ### Step Two: Start the game

    # In[ ]:
    while rounds < 2:
        game(turn,3*number_of_players, list_of_players)
        for cp in list_of_players:
            for idx,com in enumerate(list_of_companies.keys()):
                ans = filter(lambda x: x.card_company == com,cp.player_cards)
                final = sum(list(map(lambda x: x.card_value, list(ans))))
                com_name_list[idx].company_current_price += final
                
        for c in com_name_list:
            c.company_current_price = max(c.company_current_price, 0)
            
        
        print("\nEnd of Round {}\n".format(rounds+1))
        print(list(map(lambda x: {x.company_name:x.company_current_price},com_name_list)))
        time.sleep(7)
        turn = 0
        next(current_turn)
        assign_cards(list_of_cards,list_of_players)
        rounds += 1
        
    for current_player in list_of_players:
        for shares in current_player.player_shares.keys():
            current_player.player_amount += current_player.player_shares[shares] * list_of_companies[shares]
            
    for current_player in list_of_players:
        print("Name : {} \t Amount : {}".format(current_player.player_name,current_player.player_amount))
        print("Current Shares : {}".format(current_player.player_shares))
