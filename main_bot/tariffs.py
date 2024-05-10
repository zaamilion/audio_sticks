class Tarif:
    def __init__(self, name: str, quantity_of_bots: int, price: int, bot_tarifs: dict):# {BotTarif: int}}
        self.name = name
        self.quantity = quantity_of_bots
        self.price = price
        self.bot_tarifs = bot_tarifs

class BotTarif:
    def __init__(self, name, quantity, id):
        self.name = name
        self.quantity = quantity
bot_default = BotTarif(name='Стандартный', quantity=5, id='bot_default')
bot_lite = BotTarif(name='Лайт', quantity=15, id='bot_lite')
bot_premium = BotTarif(name='Премиум', quantity=25, id='bot_premium')
bot_maximum = BotTarif(name='Максимум', quantity=50, id='bot_maximum')

default = Tarif(name='Стандартный', quantity_of_bots=1, price=0, bot_tarifs={bot_default: 1})
optimal = Tarif(name='Оптимальный', quantity_of_bots=1, price=50, bot_tarifs={bot_lite: 1})
botovod = Tarif(name='Ботовод', quantity_of_bots=3, price=75, bot_tarifs={bot_default:1, bot_lite:2})
big = Tarif(name='Большой', quantity_of_bots=3, price=100, bot_tarifs={bot_lite:1, bot_premium:2})
premium = Tarif(name='Премиум', quantity_of_bots=4, price=149, bot_tarifs={bot_premium:4})
huge = Tarif(name='Огромный', quantity_of_bots=5, price=199, bot_tarifs={bot_premium:4, bot_maximum:1})
nonfull = Tarif(name='НеФулл', quantity_of_bots=8, price=259, bot_tarifs={bot_premium:4, bot_maximum:4})
maximal = Tarif(name='Максимум', quantity_of_bots=10, price=500, bot_tarifs={bot_maximum:10})