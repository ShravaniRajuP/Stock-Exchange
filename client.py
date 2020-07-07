import socket
import json
from Classes import Player, Cards, Company

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# Response = ClientSocket.recv(1024)
# print(Response.decode('utf-8'))

def host_file():
    Input = input("Number of players: ")
    ClientSocket.send(str.encode(Input))

def non_hostfile():
    print("Waiting for the host to start the game.")

def print_price_list(com_name_list):
    print(list(map(lambda x: {x.company_name: x.company_current_price},com_name_list)))


def player_choice():
    # print("\nPrice List: ", end="")
    # print_price_list(com_name_list)
    choice = input("\nEnter your choice(buy/sell/pass): ")
    if choice == 'pass' or choice == '':
        # print('pass')
        ClientSocket.send(str.encode(choice))
        return
    elif choice == 'buy' or choice == 'sell':
        print("\n")
        print(list(map(lambda x: x.company_name,com_name_list)))
        com_num = input("Enter the company number: ")
        shares = input("Enter the number of shares: ")
        # print(choice, com_num, shares)
        ClientSocket.send(str.encode(choice +','+ com_num +','+ shares))
        # print_trade(current_player, company, 'after', shares, choice)
    else:
        # print('fail')
        player_choice()
    

def wait():
    pass

def check_response(data):
    # print(data)
    if data == 'host':
        host_file()
    elif data == 'play':
        player_choice()
    elif data == 'wait':
        wait()
    elif data == 'update':
        # print(data)
        # global com_name_list
        for i in range(len(com_name_list)):
            change = ClientSocket.recv(1024).decode('utf-8')
            com_name_list[i].company_current_price = change
            
        print_price_list(com_name_list)
    # elif data == 'json':
    #     # b = b'' + ClientSocket.recv(1024)
    #     # Response = json.loads(b.decode('utf-8'))
    #     # Response = ClientSocket.recv(1024).decode('utf-8')
    #     print(Response)
    else:
        print(data)
        # print(data)
        # non_hostfile()
    return

Input = input('Enter Your Name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024).decode('utf-8')
check_response(Response)
print_price_list(com_name_list)
while True:
    Response = ClientSocket.recv(1024).decode('utf-8')
    check_response(Response)


ClientSocket.close()