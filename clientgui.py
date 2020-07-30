from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivy.clock import Clock

class CardsLayout(GridLayout):
    def __init__(self, **kwargs):
        super(CardsLayout, self).__init__(**kwargs)
        for i in range(22):
            self.add_widget(Label(text=str(i),color=(0,0,0,1)))

class ChoiceLayout(DropDown):
    pass

class CompanyLayout(DropDown):
    pass


class OptionLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(OptionLayout,self).__init__(**kwargs)
        self.dropdown1 = ChoiceLayout()
        self.mainbutton1 = Button(text ='Choice',
                                 size_hint_x = 1, size_hint_y = None, height = 30)
        self.add_widget(self.mainbutton1)
        self.mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(on_select=lambda \
                instance, x: setattr(self.mainbutton1, 'text', x))

        self.dropdown2 = CompanyLayout()
        self.mainbutton2 = Button(text='Company',
                                  size_hint_x=1, size_hint_y=None, height = 30)
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


class PlayerDetailsLayout(GridLayout):
    pass

class PriceListLayout(GridLayout):
    pass

class RootWidget(BoxLayout):
   pass

class Client(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Client().run()