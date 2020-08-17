from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.clock import Clock

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
   pass

class Client(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Client().run()