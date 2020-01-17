from random import randint
from time import sleep
from os import system


cards_avail = [4]*13
cards_shape = [['Clubs','Spade','Diamond','Hearts']]
for i in range(1,13):
    cards_shape.append(['Clubs','Spade','Diamond','Hearts'])

class Card():

    value = 0
    def pick_number(self):
        while True:
            card_n = randint(1,13)
            if cards_avail[card_n-1] > 0:
                cards_avail[card_n-1] -= 1
                self.number = card_n
                break
    def pick_shape(self):           #function to assign shape
        temp = randint(0,len(cards_shape[self.number-1])-1)
        self.shape = cards_shape[self.number-1][temp]
        cards_shape[self.number-1].pop(temp)
        self.name = str(self.number) + ' of ' + self.shape
    def assign_value(self):
        if self.number >=2 and self.number <=10:
            self.value = self.number
        else:
            self.value = 10
    def __str__(self):
        return self.name
    def __int__(self):
        return self.number
    

#Base class for computer and humanplayer
class Player():

    total_value = 0
    name = ""
    def pick_card(self):
        card_picked = Card()
        card_picked.pick_number()
        card_picked.pick_shape()
        return card_picked

    def __str__(self):
        return self.name
    
    


    

class HumanPlayer(Player):

    
    cards = []
    def getname(self):
        self.name = input('Please enter your name : ')
        print(f'Welcome {self.name}!')
    

    def start(self):
        card1 = self.pick_card()
        card2 = self.pick_card()

        print(f'{self.name} got a {card1.name} and {card2.name} to start with')
        if card1.number == 1:
            card1.value = int(input('As you got an ace how do you want to use it ? (1 or 11): '))
        else:
            card1.assign_value()
        if card2.number == 1:
            card2.value = int(input('As you got an ace how do you want to use it ? (1 or 11): '))
        else:
            card2.assign_value()
        self.cards.append(card1)
        self.cards.append(card2)
        self.total_value += card1.value + card2.value

    def hit(self):

        card = self.pick_card()
        print(f'{self.name} hit got a {card.name}')
        if card.number == 1:
            card.value = int(input('As you got an ace how do you want to use it ? (1 or 11): '))
        else:
            card.assign_value()
        self.cards.append(card)
        self.total_value += card.value

    def display(self):
        sleep(3)
        system('clear')
        print(f'{self.name} has -->')
        for card in self.cards:
            print('A ' + str(card))
        print(f'And total value : {self.total_value}')
    
    def check_bust(self):
        if self.total_value >= 21:
            return True
        return False

            

class Computer(Player):

    cards = []
    def __init__(self):
        self.name = "Computer Dealer"

    def process_card(self):
        card = self.pick_card()
        print(f'{self.name} got a {card}')
        if card == 1:
            if self.total_value < 10 :
                card.value = 11
            else:
                card.value = 1
        else:
            card.assign_value()
        self.cards.append(card)
        self.total_value += card.value
   
    def start(self):
        self.process_card()
    
    def hit(self):
        self.process_card()

    def display(self):
        sleep(3)
        system('clear')
        print(f'{self.name} has -->')
        for card in self.cards:
            print('A ' + str(card))
        print(f'And total value : {self.total_value}')
    
    def check_bust(self):
        if self.total_value >= 21:
            return True
        return False


player = HumanPlayer()
computer = Computer()

def playerplays():

    player.display()
    choice = input(f'{player.name} do want to hit ? (y/n)').lower()
    if choice == 'y':
        player.hit()
    else:
        print(f'{player.name} stays ')
    return choice == 'y'


#main 

print('Welcome to black jack')
player.getname()
player.start()
computer.start()

while True:

    ch = playerplays()
    if player.check_bust():
        print(f'{player.name} got busted!! \n {computer.name} WON!!! ')
        break
    if ch == 0:
        while not computer.check_bust() and computer.total_value < player.total_value:
            computer.display()
            computer.hit()
        if computer.check_bust():
            print(f'Computer got busted \n {player.name} WON !!! ')
        else:
            print(f"Computer won !! {player.name}'s total value({player.total_value}) is now less than computer's total value({computer.total_value})")  
        break



    