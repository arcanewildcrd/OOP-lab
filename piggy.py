'''coins = 100

#add 500
coins_new = 100 + 500
print(coins_new)'''

class Piggy_bank:
    def __init__(self, coins):
        self._coins = coins
        self.put_in(coins)
    
    
    def put_in(self, amount):
        if amount <= 0:
            raise ValueError("Add real Money, punk!")
        self._coins += amount
        
    def take_out(self, amount):
        if amount <= 0:
            raise ValueError("Negative! GO TO WORK!")
        if amount > self._coins:
            raise ValueError("Today's ur lucky day!")
        self._coins -= amount   
    
    def how_much(self):
        return self._coins
    
    
    
    
    

murayama = Piggy_bank(coins=100000)
murayama.put_in(40000)

murayama._coins = -50000  # BAD!



print("Murayama's piggy has:", murayama.how_much(), "yen")
































































































