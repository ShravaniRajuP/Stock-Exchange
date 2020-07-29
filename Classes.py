class Player():
    def __init__(self, name, conn = None, amount = 600000):
        self.player_name = name
        self.player_amount = amount
        self.player_cards = []
        self.player_shares = {}
        self.player_connection = conn

    def __str__(self):
        return self.player_name

class Cards():
    def __init__(self, company, value):
        self.card_company = company
        self.card_value = value
    
class Company():
    def __init__(self, name, sp):
        self.company_name = name
        self.company_starting_price = sp
        self.company_current_price = sp
        self.company_total_buy_shares = 200000
        self.company_total_sell_shares = 200000
        self.company_owner = None
        self.company_director = []

    def __str__(self):
        return self.company_name