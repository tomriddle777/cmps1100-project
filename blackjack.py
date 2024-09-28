import random, time

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

def create_deck(num):
    list = []
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    for i in range(1, num + 1):
        for suit in suits:
            for i in range(1, 14):
                card = Card(i, suit)
                list.append(card)
    return list

def deck_deal(cards_list):
    global deck
    if len(deck) >= 1:
        card = deck[0]
        deck.remove(card)
        cards_list.append(card)
        return card
    else: #creates a new deck and shuffles if there's no more cards, then deal like usual
        deck = create_deck(6)
        random.shuffle(deck)
        print("Deck shuffled.")
        card = deck[0]
        deck.remove(card)
        cards_list.append(card)
        return card
    
deck = create_deck(6)
random.shuffle(deck)
    
class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.total = 0
        self.eleven = 0 #number of aces turned to 11

    def count(self):
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
        card = deck_deal(self.cards)
        self.count()
        print(self.name + " was dealt the " + card.display())
        print("Shoe size: around " + str(round((len(deck) / 312) * 100)) + "%")
        return card
    
    def silent_deal(self):
        card = deck_deal(self.cards)
        self.count()
        print(self.name + " was dealt a facedown card")
        return card
    
    def reset(self):
        self.cards = []
        self.total = 0
        self.eleven = 0

    def rig(self, num):
        card = Card(num, "Rigged")
        self.cards.append(card)
        self.count()
        print(self.name + " was dealt the " + card.display())

class Player:
    def __init__(self, name):
        self.name = name
        self.bankroll = 1000
        self.wager = 0
        self.hand = Hand(name)
        self.state = "pre"
    
    def display_hand(self):
        print("\n------------------------------------------------")
        print(f"{self.name}'s hand:")
        for card in self.hand.cards:
            print(card.display())
        print(f"Total value: {self.hand.display_count()}")
        print("------------------------------------------------\n")
        time.sleep(1)

    def hit(self):
        self.hand.deal()
        self.display_hand()
    
    def initial_deal(self):
        self.hand.deal()
    
    def input_wager(self, option):
        self.wager = option
        if option > 1:
            return "You wager " + str(self.wager) + " chips."
        else:
            return "You wager 1 chip."
    
    def bankroll_size(self):
        if self.bankroll > 1:
            return "You have " + str(self.bankroll) + " chips."
        elif self.bankroll == 1:
            return "You have 1 chip."
        else:
            return "Bankrupt."
    
    def end_round(self):
        self.hand.reset()
        self.state = "pre"
        self.wager = 0

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        self.facedown = 0
    
    def display_hand(self):
        if self.state != "pre":
            super().display_hand()
        else:
            print("\n------------------------------------------------")
            print(f"{self.name}'s hand:")
            print(self.hand.cards[0].display())
            print("Facedown card")
            print("------------------------------------------------\n")
            time.sleep(1)
    
    def hit(self):
        self.hand.deal()
        self.display_hand()

    def initial_deal(self):
        if self.facedown != 1:
            self.hand.deal()
            self.facedown += 1
        else:
            self.hand.silent_deal()
            self.facedown += 1

    def end_round(self):
        super().end_round()
        self.facedown = 0

player = Player("Player 1")
dealer = Dealer()

print("------------------------------------------------")
print("Welcome to Blackjack!\nBlackjack pays 3:2 and dealer stands on soft 17.")
print("------------------------------------------------")

def input_wager():
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
        print(player.input_wager(option))
    else:
        return "You have no more money."


def game():
    print(player.bankroll_size())

    state = input_wager()
    if state == "You have no more money.":
        return "You have no more money."

    time.sleep(0.5)
    player.initial_deal()
    time.sleep(0.5)
    dealer.initial_deal()
    time.sleep(0.5)
    player.initial_deal()
    time.sleep(0.5)
    
    dealer.initial_deal()
    dealer.display_hand()
    player.display_hand()

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
    
    dealer.state = "turn"
    dealer.display_hand()
    while dealer.hand.total < 17 or (dealer.hand.total == 17 and any(card.value == '1' for card in dealer.hand.cards)):
        dealer.hit()
        if dealer.hand.total > 21:
            player.bankroll += player.wager
            return "Dealer busts! You win!"
    print("Dealer stands.")
    
    if dealer.hand.total > player.hand.total:
        player.bankroll -= player.wager
        return "Dealer wins!"
    elif dealer.hand.total < player.hand.total:
        player.bankroll += player.wager
        return "Player wins!"
    else:
        return "It's a tie!"
    
if __name__ == "__main__":
    while player.bankroll_size() != "Bankrupt.":
        print(game())
        player.end_round()
        dealer.end_round()
        if player.bankroll_size() == "Bankrupt.":
            print("Brankrupt.")

