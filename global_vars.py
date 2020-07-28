from Classes import Company
import socket

ServerSocket, host, port = None, None, None
clients = {}
host_name = None
list_of_companies = {}
com_name_list = []
list_of_cards = []
current_turn = None
card_list = []
share_suspend_holder = None

def set_serversocket():
    global ServerSocket
    ServerSocket = socket.socket()

def get_serversocket():
    return ServerSocket

def set_host_port(h, p):
    global host, port
    host, port = h, p

def get_host_port():
    return host, port

def set_clients(name, client):
    clients[name] = client

def get_clients():
    return clients

def set_host_name(h):
    global host_name
    host_name = h

def get_host_name():
    return host_name

def set_loco_first(loco):
    global list_of_companies
    list_of_companies = loco

def set_loco_part(key, value):
    global list_of_companies
    list_of_companies[key] = value

def get_loco():
    return list_of_companies

def set_cnl_first():
    global com_name_list
    global list_of_companies
    com_name_list = [Company(company,price) for company,price in list_of_companies.items()]

def set_cnl_part(index, value):
    global com_name_list
    com_name_list[index] = value

def get_cnl():
    return com_name_list

def set_loca_full(cards):
    global list_of_cards
    list_of_cards = cards

def set_loca_part(index, value):
    global list_of_cards
    list_of_cards[index] = value

def get_loca():
    return list_of_cards

def set_current_turn(turn):
    global current_turn
    current_turn = turn

def get_current_turn():
    return current_turn

def set_card_list_full(cards):
    global card_list
    card_list = cards

def set_card_list_part(index, value):
    global card_list
    card_list[index] = value

def get_card_list():
    return card_list

def set_ss_holder(holder):
    global share_suspend_holder
    share_suspend_holder = holder

def get_ss_holder():
    return share_suspend_holder