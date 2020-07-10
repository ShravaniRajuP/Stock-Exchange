import socket
import json
from Classes import Player, Cards, Company

ClientSocket = socket.socket()
ip = input("Enter the server Ip address : ")
# host = '192.168.0.21' # Hardik's IP
# host = '192.168.0.14' # Shravani's IP
host = ip
port = 1233

list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def host_file():
    Input = input("Number of players: ")
    ClientSocket.send(str.encode(Input))

def non_hostfile():
    print("Waiting for the host to start the game.")

def print_price_list(com_name_list):
    # print(list(map(lambda x: {x.company_name: x.company_current_price},com_name_list)))
    print()
    for company in com_name_list:
        print(company.company_name, company.company_current_price, sep=': ', end='    ')
    print()

def player_choice():
    print("\nPrice List: ", end="")
    print_price_list(com_name_list)
    choice = input("\nEnter your choice(buy/sell/pass): ")
    if choice == 'pass' or choice == '':
        # print('pass')
        ClientSocket.send(str.encode(choice))
        return
    elif choice == 'buy' or choice == 'sell':
        print("\n")
        com_num = input("Enter the company number (1. Wockhardt, 2. HDFC, 3. TATA, 4. ONGC, 5. Reliance, 6. Infosys): ")
        shares = input("Enter the number of shares: ")
        ClientSocket.send(str.encode(choice +', '+ com_num +', '+ shares))
        print(choice, shares, com_num)
    else:
        player_choice()

def wait(data):
    name = data.split(" ")
    print(name[1] + " playing......")

def check_response(data):
    if data == 'host':
        host_file()
    elif data == 'play':
        player_choice()
    elif data.startswith('wait'):
        wait(data)
    elif data == 'update':
        for i in range(len(com_name_list)):
            change = ClientSocket.recv(1024).decode('utf-8')
            com_name_list[i].company_current_price = change
        print_price_list(com_name_list)
    elif data == 'Cards':
        print()
        for i in range(10):
            b = b'' + ClientSocket.recv(1024)
            card = json.loads(b.decode('utf-8'))
            space_len = 12 - len(list(card.keys())[0])
            print(list(card.keys())[0], list(card.values())[0], sep=' : ' + ' '*space_len, end='\n')
    else:
        print(data)
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