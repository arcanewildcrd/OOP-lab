class Player:
    def __init__(self, name, attack_power, health):
        self.name = name
        self.attack_power = attack_power
        self.health = 100

    
    def attack (self, other):
        other.health -= self.attack_power
        print(f'{self.name} attacks {other.name} for {self.attack_power} damage')
    
    def heal (self, amount):
        self.health += amount
        print(f'{self.name} heals for {amount} health!')
    
    
        
    def is_alive(self):
        return self.health > 0
    
player1 = Player('Fujio', attack_power=23, health=100)
player2 = Player('Murayama', attack_power=19, health=100)

print(f'-_-_-->>>>>>High and Low: Amargeddon<<<<<<--_-_-')
print(f'<<<<<<<Start Game>>>>>>>')
round_num = 1
while player1.is_alive() and player2.is_alive():
    print(f'-----Round {round_num}, Fight!----')
    player1.attack(player2)
    if not player2.is_alive():
        print(f'{player2.name} has been defeated!')
        break
    player2.attack(player1)
    if not player1.is_alive():
        print(f'{player1.name} has been defeated!')
        break
    
    print(f'{player1.name}: health = {player1.health}')
    print(f'{player2.name}: health = {player2.health}')
    round_num +=1
    
if player1.is_alive():
    print(f'---{player1.name} Wins!!!---')
if player2.is_alive():
    print(f'---{player2.name} Wins!!!---') 
    print(f'>>>VICTORY<<<') 
          
print('----Game Over!!----')    
        