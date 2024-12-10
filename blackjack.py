import random, time

def pause(seconds):
    if seconds == 0.5:
        time.sleep(0.5)
    elif seconds == 1:
        time.sleep(1)
    elif seconds == 2:
        time.sleep(2)

class Counting:
    def __init__(self, shoe):
        self.running_count = 0
        self.shoe = shoe
    
    def count(self, card):
        if card.value == 1:
            self.running_count -= 1
        elif card.value >= 10:
            self.running_count -= 1
        elif card.value >= 7:
            pass
        elif card.value <= 6:
            self.running_count += 1
    
    def reset(self):
        self.running_count = 0
    
    def display(self):
        print("----------------------------------------------------------------------")
        print("Shoe Size (until cutoff card): around " + str(round((((self.shoe.length() - 1 - ((52 * self.shoe.decks) - self.shoe.last)) / self.shoe.last) * 100), 2)) + "%")
        print("True Count: " + str(round((self.running_count / (self.shoe.length() / 52)), 2)))
        print("Running Count: " + str(self.running_count))
        print("Decks: " + str(round(((self.shoe.length() - 1) / 52), 2)))
        print("----------------------------------------------------------------------\n")

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

class Shoe:
    def __init__(self, decks, shuffle=True):
        self.decks = decks
        self.shoe = [] #stack used for game
        self.last = 0 #last card to be dealt
        self.pen = 0 #percentage of deck to be dealt
        self.counting = Counting(self)
        self.create_decks(shuffle)

    def length(self):
        return len(self.shoe)
    
    def create_decks(self, shuffle=True):
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        for i in range(1, self.decks + 1):
            for suit in suits:
                for i in range(1, 14):
                    card = Card(i, suit)
                    self.shoe.append(card)
        if shuffle:
            random.shuffle(self.shoe)
            self.cut()

    def cut(self):
        while True:
            choice = input("Where do you want to cut? Type any positive number between 0 and 10, exclusive. The lower the number is, the lower the place where dealer cut is, and vice versa. ")
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
        print("\nThe dealer cuts the deck as you requested, at around " + str(percent) + "% the size of the shoe.")

        pause(1)

        rand = random.randint(75, 95)
        index = round((52 * self.decks - 1) * (rand / 100))
        self.shoe.insert(index, Card(-1, "END"))
        self.last = index
        self.pen = round(self.last / (52 * self.decks), 4) * 100
        print("The dealer then places a plastic cutoff card at around " + str(self.pen) + "% the size of the shoe.\n")

        pause(1)

    def deal(self):
        card = self.shoe[0]
        if card.value == -1:
            print("End of shoe. Shuffling.")
            pause(1)
            self.counting.reset()
            self.shoe = []
            self.create_decks()
            card = self.shoe[0]
        self.shoe.remove(card)
        return card

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
    
    def display_sum(self, split):
        if not split:
            if len(self.cards) == 2 and self.total == 21:
                return ("Blackjack!")
        if self.total == 21:
            return ("21")
        elif self.eleven > 0:
            return ("Soft " + str(self.total))
        else:
            return self.total

    def deal(self, shoe): #different from the deal() in Shoe class
        card = shoe.deal()
        self.cards.append(card)
        self.sum()
        pause(0.5)
        return card
    
    def reset(self):
        self.cards = []
        self.total = 0
        self.eleven = 0

    def rig(self, num): #to test
        card = Card(num, "Rigged")
        self.cards.append(card)
        self.sum()
        print(self.name + " was dealt the " + card.display())

class Player:
    def __init__(self, name, shoe):
        self.name = name
        self.hand = Hand(name)
        self.state = "pre"
        self.shoe = shoe
        self.counting = shoe.counting
    
    def display_hand(self):
        print("----------------------------------------------------------------------")
        print(self.name + "'s hand:")
        for card in self.hand.cards:
            print(card.display())
        print("Total value: " + str(self.hand.display_sum(False)))
        print("----------------------------------------------------------------------\n")
        self.counting.display()
        pause(2)

    def hit(self):
        card = self.hand.deal(self.shoe)
        self.counting.count(card)
        print("----------------------------------------------------------------------")
        print(self.name + " was dealt the " + card.display())
        print("----------------------------------------------------------------------\n")
        self.display_hand()

    def initial_deal(self):
        card = self.hand.deal(self.shoe)
        self.counting.count(card)
        print(self.name + " was dealt the " + card.display())

    def end_round(self):
        self.hand.reset()
        self.state = "pre"

class Human(Player):
    def __init__(self, name, shoe):
        super().__init__(name, shoe)
        self.bankroll = float(1000)
        self.wager = 0
        self.wager2 = 0
        self.hand2 = Hand("2nd")
    
    def split_check(self):
        if (len(self.hand.cards) == 2):
            if (self.hand.cards[0].value == self.hand.cards[1].value) or (self.hand.cards[0].value >= 10 and self.hand.cards[1].value >= 10): #also split if its 10 and 13, for example.
                if self.wager <= (self.bankroll -  self.wager):
                    return True
        return False

    def split(self):
        self.hand2.cards.append(self.hand.cards[0])
        self.wager2 = self.wager
        self.hand.cards = self.hand.cards[1::]

    def display_hand(self):
        print("----------------------------------------------------------------------")
        if len(self.hand2.cards) > 0:
            print(self.name + "'s first hand:")
        else:
            print(self.name + "'s hand:")
        for card in self.hand.cards:
            print(card.display())
        print("Total value: " + str(self.hand.display_sum(len(self.hand2.cards) > 0)))
        print("----------------------------------------------------------------------\n")
        self.counting.display()
        pause(2)

    def display_hand2(self):
        print("----------------------------------------------------------------------")
        print(self.name + "'s second hand:")
        for card in self.hand2.cards:
            print(card.display())
        print("Total value: " + str(self.hand2.display_sum(len(self.hand2.cards) > 0)))
        print("----------------------------------------------------------------------\n")
        self.counting.display()
        pause(2)

    def hit(self):
        if len(self.hand2.cards) > 0:
            card = self.hand.deal(self.shoe)
            self.counting.count(card)
            print("----------------------------------------------------------------------")
            print(self.name + " was dealt the " + card.display() + " for their first hand.")
            print("----------------------------------------------------------------------\n")
            self.display_hand()
        else:
            super().hit()

    def hit2(self):
        card = self.hand2.deal(self.shoe)
        self.counting.count(card)
        print("----------------------------------------------------------------------")
        print(self.name + " was dealt the " + card.display() + " for their second hand.")
        print("----------------------------------------------------------------------\n")
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
    def __init__(self, shoe):
        super().__init__("Dealer", shoe)
        self.facedown = 0
        self.facedown_card = 0

    def display_hand(self):
        if self.state != "pre":
            super().display_hand()
        else:
            print("----------------------------------------------------------------------")
            print(self.name + "'s hand:")
            print(self.hand.cards[0].display())
            print("Facedown card")
            print("----------------------------------------------------------------------\n")

    def initial_deal(self):
        if self.facedown != 1:
            super().initial_deal()
            self.facedown += 1
        else:
            self.facedown_card = self.hand.deal(self.shoe)
            print(self.name + " was dealt a facedown card")
            self.facedown += 1

    def turn(self):
        self.state = "turn"
        print("----------------------------------------------------------------------")
        print("Dealer flips over his facedown card. It is the " + self.facedown_card.display() + ".")
        print("----------------------------------------------------------------------\n")
        self.counting.count(self.facedown_card)
        self.display_hand()

    def end_round(self):
        super().end_round()
        self.facedown = 0
        self.facedown_card = 0
    
def bet(player):
    if player.bankroll_size() != "Bankrupt":
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

def natural(player, dealer, wager):
    player_natural = (player.hand.total == 21)
    dealer_natural = (dealer.hand.total == 21)
    if (dealer_natural == True) and (player_natural == True):
        return ["T BJ", wager]
    elif (dealer_natural == True) and (player_natural == False):
        return ["L BJ", wager]
    elif (dealer_natural == False) and (player_natural == True):
        return ["W BJ", wager]
    else: 
        return [0, 0]

def compare(hand, dealer, dealer_result, wager):
    if dealer_result == "B":
        return ["W", wager]
    elif dealer.hand.total > hand.total:
        return ["L", wager]
    elif dealer.hand.total < hand.total:
        return ["W", wager]
    else:
        return ["T", wager]

def insurance(player, dealer):
    while True:
        if not (player.wager / 2) <= (player.bankroll - player.wager):
            return [0, 0]
        option = input("Do you want insurance? [y] yes, or [n] no. ")
        if option == 'y':
            print("You enter a side bet of half your original bet (" + str(player.wager / 2) + " chips) that the dealer will have a blackjack.")
            pause(1)
            if dealer.hand.total == 21:
                player.bankroll += player.wager
                print("The dealer did indeed have blackjack. Nice save! You win " + str(player.wager) + " chips!")
                return ["W", (player.wager / 2)]
            else:
                player.bankroll -= (player.wager / 2)
                print("The dealer did not have blackjack. You lose " + str(player.wager / 2) + " chips.")
                return ["L", (player.wager / 2)]
        elif option == 'n':
            print("You decline to take insurance.")
            return [0, 0]
        else:
            print("Invalid input. Please enter [y] or [n].")

def game_round(player, dealer, shoe):
    result1 = [0, 0]
    result2 = [0, 0]
    insure_result = [0, 0]
    dealer_result = ""

    bet(player)
    pause(1)
    player.initial_deal()
    dealer.initial_deal()
    player.initial_deal()
    dealer.initial_deal()
    pause(1)
    print()
    dealer.display_hand()
    player.display_hand()

    if (dealer.hand.cards[0].value == 1):
        insure_result = insurance(player, dealer)
    
    result1 = natural(player, dealer, player.wager)
    
    temp = {"W BJ": "You have blackjack! You stand.", "L BJ": "Dealer has blackjack. You lose.", "T BJ": "You both have blackjack. Push(tie)."}
    if result1[0] in temp.keys():
        print(temp[result1[0]])
    
    if result1[0] not in temp.keys():
        while True:
            option = input("Would you like to surrender? [y] yes, or [n] no. ")
            if option == 'y':
                player.bankroll -= (player.wager / 2)
                print("You forfeit half of your wager and your hand.")
                result1 = ["Surrender", player.wager]
                break
            elif option =='n':
                break
            else:
                print("Invalid input. Please choose a valid option.")

    while result1[0] == 0: #if neither has a blackjack
        if (player.split_check() == False):
            if (player.hand.total >= 9) and (player.hand.total <= 11) and (player.wager <= (player.bankroll - player.wager)):
                while True:
                    option = input("What would you like to do? [h] hit, [d] double down, or [st] stand. ")
                    if (option == 'h') or (option == 'd') or (option == 'st'):
                        break
                    else:
                        print("Invalid input. Please choose a valid option.")
            else:
                while True:
                    option = input("What would you like to do? [h] hit, or [st] stand. ")    
                    if (option == 'h') or (option == 'st'):
                        break
                    else:
                        print("Invalid input. Please choose a valid option.")
        else:
            if (player.hand.total >= 9) and (player.hand.total <= 11) and (player.wager <= (player.bankroll - player.wager)):
                while True:
                    option = input("What would you like to do? [h] hit, [d] double down, [sp] split, or [st] stand. ")
                    if (option == 'h') or (option == 'd') or (option == 'sp') or (option == 'st'):
                        break
                    else:
                        print("Invalid input. Please choose a valid option.")
            else:
                while True:
                    option = input("What would you like to do? [h] hit, [sp] split, or [st] stand. ")
                    if (option == 'h') or (option == 'sp') or (option == 'st'):
                        break
                    else:
                        print("Invalid input. Please choose a valid option.")

        if option == 'h':
            player.hit()
            if player.hand.total > 21:
                player.bankroll -= player.wager
                result1 = ["B", player.wager]
                print("You bust. Dealer wins. You lose " + str(result1[1]) + " chips.")
                break
            elif player.hand.total == 21:
                print("You have 21! You stand.")
                break
        elif option == 'd':
            player.wager *= 2
            print("You increase your wager to " + str(player.wager) + " chips.")
            player.hit()
            if player.hand.total > 21:
                player.bankroll -= player.wager
                result1 = ["B", player.wager]
                print("You bust. Dealer wins. You lose " + str(result1[1]) + " chips.")
                break
            else:
                print("You cannot hit anymore in this round.")
                break
        elif option == 'st':
            print("You stand.")
            break
        elif option == 'sp':
            player.split()
            print("You wager another " + str(player.wager) + " chips and split your hand.")
            player.hit()
            player.hit2()
            print("Playing your first hand.")
            while True:
                if player.hand.cards[0].value == 1:
                    option = 'st' #can only stand
                    print("You can only stand after splitting aces.")
                    pause(1)
                elif (player.hand.total >= 9) and (player.hand.total <= 11) and (player.wager <= (player.bankroll - player.wager - player.wager2)):
                    while True:
                        option = input("What would you like to do? [h] hit, [d] double down, or [st] stand. ")
                        if (option == 'h') or (option == 'd') or (option == 'st'):
                            break
                        else:
                            print("Invalid input. Please choose a valid option.")
                else:
                    while True:
                        option = input("What would you like to do? [h] hit, or [st] stand. ")    
                        if (option == 'h') or (option == 'st'):
                            break
                        else:
                            print("Invalid input. Please choose a valid option.")
                
                if option == 'h':
                    player.hit()
                    if player.hand.total > 21:
                        player.bankroll -= player.wager
                        result1 = ["B", player.wager]
                        print("You bust. Dealer wins. You lose " + str(result1[1]) + " chips.")
                        break
                    elif player.hand.total == 21:
                        print("You have 21! You stand.")
                        break
                elif option == 'd':
                    player.wager *= 2
                    print("You increase your wager to " + str(player.wager) + " chips.")
                    player.hit()
                    if player.hand.total > 21:
                        player.bankroll -= player.wager
                        result1 = ["B", player.wager]
                        print("You bust. Dealer wins. You lose " + str(result1[1]) + " chips.")
                        break
                    else:
                        print("You cannot hit anymore for this hand.")
                        break
                elif option == 'st':
                    print("You stand.")
                    break
                
            pause(1)
        
            print("Playing your second hand.")
            while True:
                if player.hand2.cards[0].value == 1:
                    option == 'st'
                    print("You can only stand after splitting aces.")
                    pause(1)
                elif (player.hand2.total >= 9) and (player.hand2.total <= 11) and (player.wager2 <= (player.bankroll - player.wager - player.wager2)):
                    while True:
                        option = input("What would you like to do? [h] hit, [d] double down, or [st] stand. ")
                        if (option == 'h') or (option == 'd') or (option == 'st'):
                            break
                        else:
                            print("Invalid input. Please choose a valid option.")
                else:
                    while True:
                        option = input("What would you like to do? [h] hit, or [st] stand. ")    
                        if (option == 'h') or (option == 'st'):
                            break
                        else:
                            print("Invalid input. Please choose a valid option.")
                
                if option == 'h':
                    player.hit2()
                    if player.hand2.total > 21:
                        player.bankroll -= player.wager2
                        result1 = ["B", player.wager2]
                        print("You bust. Dealer wins. You lose " + str(result2[1]) + " chips.")
                        break
                    elif player.hand.total == 21:
                        print("You have 21! You stand.")
                        break
                elif option == 'd':
                    player.wager2 *= 2
                    print("You increase your wager to " + str(player.wager2) + " chips.")
                    player.hit2()
                    if player.hand2.total > 21:
                        player.bankroll -= player.wager2
                        result1 = ["B", player.wager2]
                        print("You bust. Dealer wins. You lose " + str(result2[1]) + " chips.")
                        break
                    else:
                        print("You cannot hit anymore for this hand.")
                        break
                elif option == 'st':
                    print("You stand.")
                    break
            pause(1)
            break
    
    pause(1)
    print()

    dealer.turn() #dealer's turn
    while dealer.hand.total < 17 or (dealer.hand.total == 17 and any(card.value == '1' for card in dealer.hand.cards)):
        dealer.hit()
        pause(0.5)
        if dealer.hand.total > 21:
            dealer.hand.total = -1
            dealer_result = "B"
            print("Dealer busts!")
            break
    if dealer_result != 'B':
        print("Dealer stands.")
    
    pause(1)
    print("\nRESULTS:")
    pause(1)

    if len(player.hand2.cards) > 0:
        temp = 0
        result1 = compare(player.hand, dealer, dealer_result, player.wager)
        result2 = compare(player.hand2, dealer, dealer_result, player.wager2)

        if result1[0] == "B":
            print("You busted your first hand. You lost " + str(result1[1]) + " chips.")
            temp -= result1[1]
        elif result1[0] == "W":
            print("You won your first hand. You win " + str(result1[1]) + " chips.")
            temp += result1[1]
            player.bankroll += player.wager
        elif result1[0] == "L":
            print("You lost your first hand. You lose " + str(result1[1]) + " chips.")
            temp -= result1[1]
            player.bankroll -= player.wager
        elif result1[0] == "T":
            print("Push. You tied your first hand. You keep your wager of " + str(result1[1]) + " chips.")
        
        if result2[0] == "B":
            print("You busted your second hand. You lose " + str(result2[1]) + " chips.")
            temp -= result2[1]
        elif result2[0] == "W":
            print("You won your second hand. You win " + str(result2[1]) + " chips.")
            temp += result2[1]
            player.bankroll += player.wager2
        elif result2[0] == "L":
            print("You lost your second hand. You lose " + str(result2[1]) + " chips.")
            temp -= result2[1]
            player.bankroll -= player.wager2
        elif result2[0] == "T":
            print("Push. You tied your second hand. You keep your wager of " + str(result2[1]) + " chips.")

        temp += (insure_result[1] * 2)

        if temp > 0:
            print("In total, you won " + str(temp) + " chips this round.")
        elif temp < 0:
            print("In total, you lost " + str(temp * -1) + " chips this round.")
        else:
            print("In total, you won and lost no chips this round.")
    
    else:
        temp = 0
        if result1[0] == "Surrender":
            print("You had surrendered your hand and forfeited half of your original wager, which calculates to a loss of " + str(player.wager / 2) + " chips.")
            temp -= (result1[1] / 2)
        elif result1[0] == "W BJ":
            print("You had blackjack! It pays 3:2, which is " + str(result1[1] * (3 / 2)) + " chips!")
            temp += result1[1] * (3 / 2)
            player.bankroll += result1[1] * (3 / 2)
        elif result1[0] == "L BJ":
            print("The dealer had blackjack. You lose " + str(result1[1]) + " chips.") 
            temp -= result1[1]
            player.bankroll -= player.wager
        elif result1[0] == "T BJ":
            print("Push. Both you and the dealer had blackjack. You keep your wager of " + str(result1[1]) + " chips.")
        elif result1[0] == "B":
            print("You busted your hand. You lose " + str(result1[1]) + " chips.")
            temp -= result1[1]
        else:
            result1 = compare(player.hand, dealer, dealer_result, player.wager)
        
        if result1[0] == "W":
            print("You won your hand. You win " + str(result1[1]) + " chips.")
            temp += result1[1]
            player.bankroll += player.wager
        elif result1[0] == "L":
            print("You lost your hand. You lose " + str(result1[1]) + " chips.")
            temp -= result1[1]
            player.bankroll -= player.wager
        elif result1[0] == "T":
            print("Push. You tied with the dealer. You keep your wager of " + str(result1[1]) + " chips.")
        
        if insure_result[0] == "L":
            temp -= insure_result[1]
        elif insure_result[0] == "W":
            temp += (insure_result[1] * 2)

        if temp > 0:
            print("In total, you won " + str(temp) + " chips this round.")
        elif temp < 0:
            print("In total, you lost " + str(temp * -1) + " chips this round.")
        else:
            print("In total, you won and lost no chips this round.")

    print()

    print("BANKROLL: " + str(player.bankroll) + " chips\n")
    shoe.counting.display()

    player.end_round()
    dealer.end_round()
    return

if __name__ == "__main__":
    print("----------------------------------------------------------------------")
    print("Welcome to Blackjack! (6 deck shoe)\nBlackjack pays 3:2\nDealer stands on soft 17\nInsurance pays 2:1\nNo resplitting\nNo surrender, hitting on aces, or blackjack after split")
    print("----------------------------------------------------------------------\n")
    shoe = Shoe(6)
    player1 = Human("Player", shoe)
    dealer1 = Dealer(shoe)
    print("BANKROLL: " + str(player1.bankroll) + " chips")
    while player1.bankroll_size() != "Bankrupt.":
        game_round(player1, dealer1, shoe)