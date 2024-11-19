"""
added more realism before the game by adding a fucntion where
player can cut like in casino games, and dealer places a card
near the end that signals the end of the shoe, triggering a 
reshuffle.

split is implemented, but pretty crudely; I think I would have 
to clean up my win conditions and wrap it into a function to 
start cleaning my code up and eventually make the code for split
cleaner and more readable

a crude version of a count is implemented, but I haven't yet 
blocked off the count when the dealer still has its second card 
covered. this would also need to be cleaned up as there is far 
too many instances of same code fragments used in different 
places.
"""
import random, time

count = 0

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def display(self):
        name = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        num = self.value
        if num in name.keys():
            num = name[num]
        return str(num) + " of " + str(self.suit)

class Decks:
    def __init__(self, decks):
        self.decks = decks
        self.shoe = [] #stack used for game
        self.last = 0 #last card to be dealt
        self.pen = 0 #percentage of deck to be dealt
        self.create_decks()

    def length(self):
        return len(self.shoe)
    
    def create_decks(self):
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        for i in range(1, self.decks + 1):
            for suit in suits:
                for i in range(1, 14):
                    card = Card(i, suit)
                    self.shoe.append(card)
        random.shuffle(self.shoe)
        self.cut()

    def cut(self):
        while True:
            choice = input("Where do you want to cut? Type any positive number between 0 and 10, exclusive. The lower the number is, the higher the cut is, and vice versa. ")
            try:
                choice = float(choice)
                if (choice > 0) and (choice < 10):
                    break
                else:
                    print("Error. Please enter a whole number between 0 and 10, exclusive.")
            except ValueError: #if input isn't a number
                print("Error. Not a number")
        
        index = int(round((52 * self.decks * (choice / 12.5)), 0)) #determines which index we cut
        temp = self.shoe[0:index] #top portion of the cut that will go to the bottom
        self.shoe = self.shoe[index:] #bottom portion of the cut that will rise to the top
        
        for i in range(0, len(temp)):
            self.shoe.append(temp[i])
        
        percent = round((index + 1) / (52 * self.decks), 4) * 100
        print("The dealer cuts the deck as you requested, at around " + str(percent) + "% the size of the shoe.")

        rand = random.randint(75, 95)
        index = round((52 * self.decks - 1) * (rand / 100))
        self.shoe.insert(index, Card(-1, "END"))
        self.last = index - 1
        self.pen = round((self.last + 1) / (52 * self.decks), 4) * 100
        print("The dealer then places a plastic cutoff card at around " + str(self.pen) + "% the size of the shoe.")

    def deal(self, hand):
        card = self.shoe[0]
        if card.value == -1:
            print("End of shoe.")
            self.create_decks()
            card = self.shoe[0]
        self.shoe.remove(card)
        hand.append(card)
        return card
        
shoe = Decks(6)

class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.total = 0
        self.eleven = 0 #number of aces turned to 11

    def sum(self):
        self.total = 0
        self.eleven = 0
        for card in self.cards:
            value = card.value
            if card.value == 1:
                self.eleven += 1
                value = 11 #if more than 1 aces turned to 11 in this loop, while loop after this should make it into a "soft" total
            elif card.value > 10:
                value = 10
            self.total += value
        while self.total > 21 and self.eleven:
            self.total -= 10
            self.eleven -= 1
        return self.total
    
    def display_count(self):
        if len(self.cards) == 2 and self.total == 21:
            return ("Blackjack!")
        if self.total == 21:
            return ("21")
        elif self.eleven > 0:
            return ("Soft " + str(self.total))
        else:
            return self.total

    def deal(self):
        card = shoe.deal(self.cards)
        self.sum()
        time.sleep(1)
        return card
    
    def silent_deal(self):
        card = shoe.deal(self.cards)
        self.sum()
        time.sleep(1)
        return card
    
    def reset(self):
        self.cards = []
        self.total = 0
        self.eleven = 0

    def rig(self, num):
        card = Card(num, "Rigged")
        self.cards.append(card)
        self.sum()
        print(self.name + " was dealt the " + card.display())

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand(name)
        self.state = "pre"
    
    def display_hand(self):
        print("------------------------------------------------")
        print(f"{self.name}'s hand:")
        for card in self.hand.cards:
            print(card.display())
        print(f"Total value: {self.hand.display_count()}")
        print("------------------------------------------------\n")
        time.sleep(2)

    def hit(self):
        global count
        card = self.hand.deal()
        if card.value == 1:
            count -= 1
        elif card.value >= 10:
            count -= 1
        elif card.value >= 7:
            pass
        elif card.value <= 6:
            count += 1

        print("------------------------------------------------")
        print(self.name + " was dealt the " + card.display())
        print("Shoe size: around " + str(round((shoe.length() / 312) * 100)) + "%")
        print("True Count: " + str(round((count / (shoe.length() / 52)), 4)))
        print("Count: " + str(count))
        print("Decks: " + str(round((shoe.length() / 52), 4)))
        print("------------------------------------------------\n")
        self.display_hand()
    
    def initial_deal(self):
        global count
        card = self.hand.deal()
        if card.value == 1:
            count -= 1
        elif card.value >= 10:
            count -= 1
        elif card.value >= 7:
            pass
        elif card.value <= 6:
            count += 1

        print("------------------------------------------------")
        print(self.name + " was dealt the " + card.display())
        print("Shoe size: around " + str(round((shoe.length() / 312) * 100)) + "%")
        print("True Count: " + str(round((count / (shoe.length() / 52)), 4)))
        print("Count: " + str(count))
        print("Decks: " + str(round((shoe.length() / 52), 4)))
        print("------------------------------------------------\n")

    def end_round(self):
        self.hand.reset()
        self.state = "pre"

class Human(Player):
    def __init__(self, name):
        super().__init__(name)
        self.bankroll = 1000
        self.wager = 0
        self.hand2 = Hand("2nd")

    def split_check(self):
        if (len(self.hand.cards) == 2) and self.hand.cards[0].value == self.hand.cards[1].value:
            return True
        return False

    def split(self):
        self.hand2.cards.append(self.hand.cards[0])
        self.hand.cards = self.hand.cards[1::]

    def display_hand2(self):
        print("------------------------------------------------")
        print(f"{self.name}'s second hand:")
        for card in self.hand2.cards:
            print(card.display())
        print(f"Total value: {self.hand2.display_count()}")
        print("------------------------------------------------\n")
        time.sleep(2)

    def hit2(self):
        global count
        card = self.hand2.deal()

        if card.value == 1:
            count -= 1
        elif card.value >= 10:
            count -= 1
        elif card.value >= 7:
            pass
        elif card.value <= 6:
            count += 1
        

        print("------------------------------------------------")
        print(self.name + " was dealt the " + card.display())
        print("Shoe size: around " + str(round((shoe.length() / 312) * 100)) + "%")
        print("True Count: " + str(round((count / (shoe.length() / 52)), 4)))
        print("Count: " + str(count))
        print("Decks: " + str(round((shoe.length() / 52), 4)))
        print("------------------------------------------------\n")
        self.display_hand2()

    def bet(self, bet):
        self.wager = bet
        if bet > 1:
            return "You bet " + str(bet) + " chips."
        else:
            return "You bet 1 chip."
    
    def bankroll_size(self):
        if self.bankroll > 1:
            return "You have " + str(self.bankroll) + " chips."
        elif self.bankroll == 1:
            return "You have 1 chip."
        else:
            return "Bankrupt."
        
    def end_round(self):
        super().end_round()
        self.hand2.reset()
        self.wager = 0

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        self.facedown = 0
    
    def display_hand(self):
        if self.state != "pre":
            super().display_hand()
        else:
            print("------------------------------------------------")
            print(f"{self.name}'s hand:")
            print(self.hand.cards[0].display())
            print("Facedown card")
            print("------------------------------------------------\n")
            time.sleep(2)

    def initial_deal(self):
        global count
        if self.facedown != 1:
            card = self.hand.deal()
            if card.value == 1:
                count -= 1
            elif card.value >= 10:
                count -= 1
            elif card.value >= 7:
                pass
            elif card.value <= 6:
                count += 1

            print("------------------------------------------------")
            print(self.name + " was dealt a facedown card")
            print("Shoe size: around " + str(round((shoe.length() / 312) * 100)) + "%")
            print("------------------------------------------------\n")
            self.facedown += 1
        else:
            card = self.hand.silent_deal()
            if card.value == 1:
                count -= 1
            elif card.value >= 10:
                count -= 1
            elif card.value >= 7:
                pass
            elif card.value <= 6:
                count += 1
        

            print("------------------------------------------------")
            print(self.name + " was dealt a facedown card")
            print("Shoe size: around " + str(round((shoe.length() / 312) * 100)) + "%")
            print("------------------------------------------------\n")
            self.facedown += 1

    def end_round(self):
        super().end_round()
        self.facedown = 0

print("------------------------------------------------")
print("Welcome to Blackjack!\nBlackjack pays 3:2 and dealer stands on soft 17.")
print("------------------------------------------------")

player = Human("Player 1")
dealer = Dealer()

def game():
    print(player.bankroll_size())
    print("Count: " + str(round((count / (shoe.length() / 52)), 4)))
    print("NEW ROUND")

    if player.bankroll != 0:
        option = 0
        while True:
            option = input("How much do you want to wager? Please type a whole number. ")
            try:
                option = int(option)
                if (int(option) > 0):
                    if (int(option) <= player.bankroll):
                        break
                    else:
                        print("Not enough money.")
                else:
                    print("Please enter a whole number greater than 0.")
            except:
                print("Please enter a whole number.")
        print(player.bet(option))
    else:
        return "You have no more money."
    
    time.sleep(1)

    player.initial_deal()
    dealer.initial_deal()
    player.initial_deal()

    
    dealer.initial_deal()
    dealer.display_hand()
    player.display_hand()

    player.hand.cards = []
    player.hand.rig(10)
    player.hand.rig(10)

    for i in range (0, 2):
        print("RIGGED VALUE:" + str(player.hand.cards[i].value))

    player_natural = player.hand.total == 21
    dealer_natural = dealer.hand.total == 21

    if (dealer_natural):
        if player_natural:
            return "Tie."
        else:
            player.bankroll -= player.wager
            return "You lose. Dealer has blackjack."
    else:
        if player_natural:
            player.bankroll += int(round(player.wager * (3 / 2)))
            return "You win! You have blackack."

    while True:
        if (player.split_check() == False):
            option = input("What would you like to do? [h] hit, or [s] stand. ")
            if option == 'h':
                player.hit()
                if player.hand.total > 21:
                    player.bankroll -= player.wager
                    return "You bust. Dealer wins."
                elif player.hand.total == 21:
                    print("You have 21! You stand.")
                    time.sleep(1)
                    break
            elif option == 's':
                print("You stand.")
                break
            else:
                print("Invalid move. Please enter 'h' or 's'.")
        else:
            option = input("What would you like to do? [h] hit, [st] stand, or [sp] split. ")
            if option == "h":
                player.hit()
                if player.hand.total > 21:
                    player.bankroll -= player.wager
                    return "You bust. Dealer wins."
                elif player.hand.total == 21:
                    print("You have 21! You stand.")
                    time.sleep(1)
                    break
            elif option == "s":
                print("You stand.")
                break
            elif option == "sp":
                print("You wager another " + str(player.wager) + " chips and split your hand.")
                player.wager *= 2
                player.split()
                print("Playing your first hand.")
                while True:
                    option = input("What would you like to do? [h] hit, or [s] stand. ")
                    if option == 'h':
                        player.hit()
                        if player.hand.total > 21:
                            player.bankroll -= player.wager
                            print("You bust. Dealer wins.")
                            break
                        elif player.hand.total == 21:
                            print("You have 21! You stand.")
                            time.sleep(1)
                            break
                    elif option == 's':
                        print("You stand.")
                        break
                    else:
                        print("Invalid move. Please enter 'h' or 's'.")

                print("Now playing second hand.")
                while True:
                    option = input("What would you like to do? [h] hit, or [s] stand. ")
                    if option == 'h':
                        player.hit2()
                        if player.hand2.total > 21:
                            player.bankroll -= player.wager
                            print("You bust. Dealer wins.")
                            break
                        elif player.hand2.total == 21:
                            print("You have 21! You stand.")
                            time.sleep(1)
                            break
                    elif option == 's':
                        print("You stand.")
                        break
                    else:
                        print("Invalid move. Please enter 'h' or 's'.")
                
                dealer.state = "turn"
                dealer.display_hand()
                while dealer.hand.total < 17 or (dealer.hand.total == 17 and any(card.value == '1' for card in dealer.hand.cards)):
                    dealer.hit()
                    if dealer.hand.total > 21:
                        dealer.hand.total = -1
                        print("Dealer busts!")
                        break
                print("Dealer stands.")
                
                print("First hand:")
                if player.hand.total > 21:
                    print("Bust.")
                elif dealer.hand.total > player.hand.total:
                    player.bankroll -= player.wager / 2
                    print("Dealer wins!")
                elif dealer.hand.total < player.hand.total:
                    player.bankroll += player.wager / 2
                    print("Player wins!")
                else:
                    print("It's a tie!")

                print("Second hand:")
                if player.hand2.total > 21:
                    print("Bust.")
                elif dealer.hand.total > player.hand2.total:
                    player.bankroll -= player.wager / 2
                    print("Dealer wins!")
                elif dealer.hand.total < player.hand2.total:
                    player.bankroll += player.wager / 2
                    print("Player wins!")
                else:
                    print("It's a tie!")

                return "End of round."

            else:
                print("Invalid move. Please enter 'h' or 's'.")
    
    dealer.state = "turn"
    dealer.display_hand()
    while dealer.hand.total < 17 or (dealer.hand.total == 17 and any(card.value == '1' for card in dealer.hand.cards)):
        dealer.hit()
        if dealer.hand.total > 21:
            player.bankroll += player.wager * 2
            return "Dealer busts!"
    print("Dealer stands.")
    
    if dealer.hand.total > player.hand.total:
        player.bankroll -= player.wager
        return "Dealer wins!"
    elif dealer.hand.total < player.hand.total:
        player.bankroll += player.wager
        return "Player wins!"
    else:
        return "It's a tie!"

while player.bankroll_size() != "Bankrupt.":
    print(game())
    player.end_round()
    dealer.end_round()
    if player.bankroll_size() == "Bankrupt.":
        print("Bankrupt.")