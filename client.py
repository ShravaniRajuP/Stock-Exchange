import socket
import json
from Classes import Player, Cards, Company

ClientSocket = socket.socket()
host = input("Enter the server Ip address : ")
# host = '192.168.0.11'
# host = '192.168.0.171'
# ip = '52.9.147.73'
port = 1233

list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
com_name_list = [Company(company,price) for company,price in list_of_companies.items()]

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def reset_price():
    global list_of_companies
    global com_name_list
    list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
    com_name_list = [Company(company,price) for company,price in list_of_companies.items()]

def host_file():
    Input = input("Number of players: ")
    if not Input or Input == '' or not Input.isdigit():
        host_file()
    else:
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
    choice = input("\nEnter your choice(buy/sell/pass/loan/rights/debenture): ")
    if choice == 'pass' or choice == '':
        # print('pass')
        ClientSocket.send(str.encode(choice))
        return
    elif choice == 'buy' or choice == 'sell' or choice == 'ssell' or choice == 'sbuy':
        print("\n")
        # print(list(map(lambda x: x.company_name,com_name_list)))
        com_num = input("Enter the company number (1. Wockhardt, 2. HDFC, 3. TATA, 4. ONGC, 5. Reliance, 6. Infosys): ")
        shares = input("Enter the number of shares: ")
        if int(shares)%1000:
            print("Enter shares in multiple of 1000")
            shares = input("Enter the number of shares: ")
        if com_num == '' or shares == '':
            player_choice()
        else:
            ClientSocket.send(str.encode(choice +', '+ com_num +', '+ shares))
            # print(choice, shares, com_num)
    elif choice == 'loan':
        ClientSocket.send(str.encode(choice))
    elif choice == 'debenture':
        com_num = input("Enter the company number (1. Wockhardt, 2. HDFC, 3. TATA, 4. ONGC, 5. Reliance, 6. Infosys): ")
        if not com_num or com_num == '':
            player_choice()
        else:
            ClientSocket.send(str.encode(choice + ', ' + com_num))
    elif choice == 'rights':
        com_num = input("Enter the company number (1. Wockhardt, 2. HDFC, 3. TATA, 4. ONGC, 5. Reliance, 6. Infosys): ")
        if not com_num or com_num == '':
            player_choice()
        else:
            ClientSocket.send(str.encode(choice + ', ' + com_num))
    else:
        player_choice()
    return

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
    elif data == 'suspend':
        print("Entered suspend statement")
        Input = input('Do you want to use Share Suspend? (Enter Company Number / 0): ')
        if Input.isdigit() and (int(Input) < 0 or int(Input) > 6):
            check_response('suspend')
        else:
            ClientSocket.send(str.encode(Input))
    elif data == 'play again':
        Input = input("Do you want to play again(Y/N)? ")
        if Input.lower() == 'n':
            ClientSocket.send(str.encode(Input))
            return 0
        else:
            ClientSocket.send(str.encode(Input))
            reset_price()
    elif 'Shares' in data:
        print(data, end = ' ')
    elif data.startswith("RN"):
        while data != "end":
            data = ClientSocket.recv(1024).decode('utf-8')
            print(data)
        Input = input("Do you want to remove the highest negative card (Y/N)?")
        if not Input or Input == '':
            Input = input("Do you want to remove the highest negative card (Y/N)?")
        else:
            ClientSocket.send(str.encode(Input))
    elif data.startswith("dir"):
        players = data.split(' ')[1]
        Input = input("Remove highest negative card among from these players {}?".format(players))
        if not Input or Input == '':
            Input = input("Remove highest negative card among from these players {}?".format(players))
        else:
            ClientSocket.send(str.encode(Input))
    elif data.startswith("RC"):
        Input = input("{} has been share suspended. Do you want to remove share suspend (Y/N)?".format(data.split(' ')[1]))
        if not Input or Input == '':
            Input = input("{} has been share suspended. Do you want to remove share suspend (Y/N)?".format(data.split(' ')[1]))
        else:
            ClientSocket.send(str.encode(Input))
    else:
        print(data)
    return 1

flag = 1
Input = input('Enter Your Name: ')
ClientSocket.send(str.encode(Input))
Response = ClientSocket.recv(1024).decode('utf-8')
check_response(Response)
print_price_list(com_name_list)
while flag:
    Response = ClientSocket.recv(1024).decode('utf-8')
    # print(Response)
    flag = check_response(Response)
ClientSocket.close()