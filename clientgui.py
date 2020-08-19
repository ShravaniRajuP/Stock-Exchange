from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

import socket, json
from Classes import Company
from client_helper import host_file, non_hostfile, wait, set_clientsocket, \
    trade, player_choice, share_suspend, director, owner, remove_ss, print_cards

from client import *

ClientSocket = None

class CardsLayout(RecycleView):
    def __init__(self, **kwargs):
        super(CardsLayout, self).__init__(**kwargs)
        self.update_cards()

    def update_cards(self):
        table_data = []
        table_data.append({'text': str("Cards"), 'color': (0, 0, 0, 1)})
        table_data.append({'text': str("Value"), 'color': (0, 0, 0, 1)})
        for i in range(20):
            table_data.append({'text': str(i), 'color': (0, 0, 0, 1)})
        self.data = table_data

class ChoiceLayout(DropDown):
    pass

class CompanyLayout(DropDown):
    pass


class OptionLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(OptionLayout,self).__init__(**kwargs)
        self.dropdown1 = ChoiceLayout()
        self.mainbutton1 = Button(text ='Choice',
                                 size_hint_x = 1, size_hint_y = 0.3, height = 30,pos_hint ={'x':0, 'top':0})
        self.add_widget(self.mainbutton1)
        self.mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(on_select=lambda \
                instance, x: setattr(self.mainbutton1, 'text', x))

        self.dropdown2 = CompanyLayout()
        self.mainbutton2 = Button(text='Company',
                                  size_hint_x=1, size_hint_y=0.3, height = 30)
        self.add_widget(self.mainbutton2)
        self.mainbutton2.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(on_select=lambda \
                instance, x: setattr(self.mainbutton2, 'text', x))


class LogLayout(RecycleView):
    def __init__(self,**kwargs):
        super(LogLayout,self).__init__(**kwargs)
        self.update_data()

    def update_data(self):
        table_data = []
        for i in range(50):
            table_data.append({'text':str(i), 'color': (0,0,0,1)})
        self.data = table_data


class PlayerDetailsLayout(RecycleView):
    def __init__(self,**kwargs):
        super(PlayerDetailsLayout,self).__init__(**kwargs)
        self.update_data()

    def update_data(self):
        table_data = []
        for i in range(7):
            table_data.append({'text': str(i), 'color': (0, 0, 0, 1)})
        self.data = table_data

class HeaderLayout(BoxLayout):
    pass

class PriceListLayout(RecycleView):
    def __init__(self, **kwargs):
        super(PriceListLayout, self).__init__(**kwargs)
        self.update_data()

    def update_data(self):
        table_data = []
        for i in range(60):
            table_data.append({'text': str(i), 'color': (0, 0, 0, 1)})
        self.data = table_data

class RootWidget(BoxLayout):
    def change_cards(self,card_list):
        table_data = []
        table_data.append({'text': str("Cards"), 'color': (0, 0, 0, 1)})
        table_data.append({'text': str("Value"), 'color': (0, 0, 0, 1)})
        for i in card_list:
            table_data.append({'text': str(i), 'color': (0, 0, 0, 1)})
        self.cards.data = table_data

class HomeScreen(Screen):
    pass


class GameScreen(Screen):
    pass

class MainScreen(ScreenManager):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        global ClientSocket
        ClientSocket = socket.socket()

    def check_host(self):
        global ClientSocket
        ip = self.player_ip.text
        name = self.player_name.text
        try:
            ClientSocket.connect((ip, 1233))
        except socket.error as e:
            print(str(e))

        ClientSocket.send(str.encode(name))
        Response = ClientSocket.recv(8).decode('utf-8').strip()
        if Response == 'host':
            self.host_check.opacity = 1
        else:
            self.current = 'game'

    def num_of_players(self):
        num_players = self.number_players.text
        print(num_players)
        ClientSocket.send(str.encode(num_players))
        self.current = 'game'


# sm = ScreenManager()
# sm.add_widget(HomeScreen(name='home'))
# sm.add_widget(GameScreen(name='game'))

class Client(App):
    pass


if __name__ == '__main__':
    Client().run()