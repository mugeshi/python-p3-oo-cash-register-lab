class CashRegister:
    def __init__(self, discount=0):
        self.total = 0
        self.items = []
        self.discount = discount

    def add_item(self, price, quantity=1):
        for _ in range(quantity):
            self.items.append(price)
            self.total += price

    def apply_discount(self):
        if self.discount > 0:
            self.total = self.total * (1 - self.discount / 100)
            return f"After the discount, the total comes to ${self.total:.2f}."
        else:
            return "There is no discount to apply."

    def void_last_transaction(self):
        if self.items:
            last_item_price = self.items.pop(-1)
            self.total -= last_item_price
        else:
            self.total = 0

# Testing the CashRegister class
register = CashRegister()
register.add_item(10)
register.add_item(20)
register.add_item(30)

print("Total before discount:", register.total)
register.discount = 10
register.apply_discount()
print("Total after discount:", register.total)

register.void_last_transaction()
print("Total after voiding last transaction:", register.total)
