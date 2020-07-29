import json

Input = "Enter the company number (1. Wockhardt, 2. HDFC, 3. TATA, 4. ONGC, 5. Reliance, 6. Infosys): "
ClientSocket = None

def set_clientsocket(client_socket):
    global ClientSocket
    ClientSocket = client_socket

def host_file():
    Input = input("Number of players: ")
    if not Input or Input == '' or not Input.isdigit():
        host_file()
    else:
        ClientSocket.send(str.encode(Input))

def non_hostfile():
    print("Waiting for the host to start the game...")

def wait(data):
    name = data.split(" ")
    print(name[1] + " playing...")

def trade(choice):
    print("\n")
    com_num = input(Input)
    if not com_num.isdigit() or (com_num.isdigit() and (int(com_num) < 1 or int(com_num) > 6)):
        trade(choice)
        return
    shares = input("Enter the number of shares: ")
    if com_num == '' or shares == '':
        player_choice()
    elif int(shares) % 1000:
        print("Enter shares in multiples of 1000.")
        player_choice()
    else:
        ClientSocket.send(str.encode(choice + ', ' + com_num + ', ' + shares))

def player_choice():
    choice = input("\nEnter your choice (buy / sell / pass / loan / rights / debenture): ")
    if choice in ['pass', '']:
        ClientSocket.send(str.encode(choice))
    elif choice in ['buy', 'sell', 'ssell', 'sbuy']:
        trade(choice)
    elif choice == 'loan':
        ClientSocket.send(str.encode(choice))
    elif choice in ['debenture', 'rights']:
        com_num = input(Input)
        if not com_num or com_num == '':
            player_choice()
        else:
            ClientSocket.send(str.encode(choice + ', ' + com_num))
    else:
        player_choice()
    return

def print_cards():
    print()
    for _ in range(10):
        b = b'' + ClientSocket.recv(1024)
        card = json.loads(b.decode('utf-8'))
        space_len = 12 - len(list(card.keys())[0])
        print(list(card.keys())[0], list(card.values())[0], sep=' : ' + ' '*space_len, end='\n')

def share_suspend():
    print("Entered suspend statement")
    Input = input('Do you want to use Share Suspend? (If yes, Enter Company Number / If no, enter 0): ')
    if not Input or Input == '':
        share_suspend()
    elif Input.isdigit() and (int(Input) < 0 or int(Input) > 6):
        share_suspend()
    else:
        ClientSocket.send(str.encode(Input))

def owner_input():
    Input = input("Do you want to remove the highest negative card (Y/N)?")
    if not Input or Input == '':
        owner_input()
    else:
        ClientSocket.send(str.encode(Input))

def owner(data):
    while data != "end":
        data = ClientSocket.recv(1024).decode('utf-8')
        print(data)
    owner_input()

def director_input(players):
    Input = input("Remove highest negative card among from these players {}?".format(players))
    if not Input or Input == '':
        director_input(players)
    else:
        ClientSocket.send(str.encode(Input))

def director(data):
    players = data.split(' ')[1]
    director_input(players)
        
def remove_ss(data):
    Input = input("{} has been share suspended. Do you want to remove share suspend (Y/N)?".format(data.split(' ')[1]))
    if not Input or Input == '':
        remove_ss(data)
    else:
        ClientSocket.send(str.encode(Input))