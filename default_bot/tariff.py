class Tarif:
    def __init__(self, name: str, price: int, quantity: int, active=True):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = active

default = Tarif(name='Бесплатный', price=0, quantity=5)
lite = Tarif(name='Лайт', price=49, quantity=10)
premium = Tarif(name='Премиум', price=99, quantity=20)