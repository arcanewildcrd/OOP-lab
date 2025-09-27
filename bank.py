class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
     
    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        self.balance -= amount
        
        
account = BankAccount(500)
account.deposit(70)
account.withdraw(600) 
print(account.balance)               