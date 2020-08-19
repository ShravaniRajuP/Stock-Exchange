import socket, json
from Classes import Company
from client_helper import host_file, non_hostfile, wait, set_clientsocket, \
    trade, player_choice, share_suspend, director, owner, remove_ss, print_cards

list_of_companies, com_name_list = None, None

def set_price():
    set_clientsocket(ClientSocket)
    global list_of_companies
    global com_name_list
    list_of_companies = {'Wockhardt': 20, 'HDFC': 25, 'TATA': 40, 'ONGC': 55, 'Reliance': 75, 'Infosys': 80}
    com_name_list = [Company(company, price) for company, price in list_of_companies.items()]

def print_price_list():
    print()
    for company in com_name_list:
        print(company.company_name, company.company_current_price, sep=': ', end='    ')
    print()

def check_response(data):
    if data == 'host':
        host_file()
    elif data == 'play':
        print("\nPrice List: ", end="")
        print_price_list()
        player_choice()
    elif data.startswith('wait'):
        wait(data)
    elif data == 'update':
        for i in range(len(com_name_list)):
            change = ClientSocket.recv(1024).decode('utf-8')
            com_name_list[i].company_current_price = change
        print_price_list()
    elif 'Shares' in data:
        print(data, end = ' ')
    elif data == 'Cards':
        card_list = print_cards()
    elif data == 'suspend':
        share_suspend()
    elif data == 'play again':
        Input = input("Do you want to play again? (Y/N) : ")
        if Input.lower() == 'n':
            ClientSocket.send(str.encode(Input))
            return 0
        else:
            ClientSocket.send(str.encode(Input))
            set_price()
    elif data.startswith("RN"):
        owner(data)
    elif data.startswith("dir"):
        director(data)
    elif data.startswith("RC"):
        remove_ss(data)
    else:
        print(data)
    return 1

if __name__ == '__main__':
    ClientSocket = socket.socket()
    host = input("Enter the server IP address: ")
    # host = '192.168.0.11'
    # host = '192.168.0.171'
    # host = '52.9.147.73'
    port = 1233


    print('Waiting for connection...')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    set_price()
    flag = 1
    Input = input('Enter Your Name: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024).decode('utf-8')
    check_response(Response)
    print_price_list()
    while flag:
        Response = ClientSocket.recv(1024).decode('utf-8')
        flag = check_response(Response)
    ClientSocket.close()