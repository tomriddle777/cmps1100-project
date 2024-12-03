import unittest
from unittest.mock import patch
from io import StringIO

import blackjack #weird importing to lobotomize the pause function for smoother testing.

def lobotomize(seconds):
    return

blackjack.pause = lobotomize

from blackjack import *

class CreateTests(unittest.TestCase):
    def test_sanity(self): #just seeing if the way i'm testing works
        with patch('builtins.input', side_effect='5'):
            shoe1 = Shoe(1)
        shoe1.shoe = [Card(-1, "rigged")]
        self.assertEqual(shoe1.shoe[0].value, -1)
    
    def test_shuffle(self): #seeing if deck shuffles correctly after it encounters the "stop" card
        with patch('builtins.input', side_effect='5'):
            shoe1 = Shoe(1)
        shoe1.shoe = [Card(-1, "rigged")]
        self.assertEqual(len(shoe1.shoe), 1)
        with patch('builtins.input', side_effect='5'):
            shoe1.deal()
        self.assertEqual(shoe1.counting.running_count, 0)
        self.assertEqual(len(shoe1.shoe), 52 - 1 + 1)
    
    def test_count(self): #1+1+13=1+1+10=12
        obj = Hand("test")
        obj.rig(1)
        obj.rig(1)
        obj.rig(13)
        self.assertEqual(obj.sum(), 12)
    
    def test_count2(self): #1+1+1+8=11+11+11+8-10-10=21
        obj = Hand("test")
        obj.rig(1)
        obj.rig(1)
        obj.rig(1)
        obj.rig(8)
        self.assertEqual(obj.sum(), 21)

    def test_display_count(self): #see if natural blackjack has custom total count
        obj = Hand("test")
        obj.rig(1)
        obj.rig(11)
        self.assertEqual("Blackjack!", obj.display_sum(False))
    
    def test_both_bj(self): #both have BJ
        with patch('builtins.input', side_effect=['10', 'y']), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(1, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(10, "rigged"))
            shoe.shoe[3] = (Card(10, "rigged"))
            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()
        # Assert specific outputs
        self.assertIn("Push. Both you and the dealer had blackjack. You keep your wager of 10 chips.", printed_output)
        self.assertIn("In total, you won 10.0 chips this round.", printed_output)
        self.assertIn("BANKROLL: 1010.0 chips", printed_output)

    def test_dealer_bj_insurance(self):
        with patch('builtins.input', side_effect=['10', 'y']), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(10, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(9, "rigged"))
            shoe.shoe[3] = (Card(10, "rigged"))
            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()
        # Assert specific outputs
        self.assertIn("The dealer had blackjack. You lose 10 chips.", printed_output)
        self.assertIn("In total, you won and lost no chips this round.", printed_output)
        self.assertIn("BANKROLL: 1000.0 chips", printed_output)
    
    def test_bj(self):
        with patch('builtins.input', side_effect=['5', 'n']), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(10, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(1, "rigged"))
            shoe.shoe[3] = (Card(5, "rigged"))
            shoe.shoe[3] = (Card(4, "rigged")) #dealer should have 21 too, but not natural
            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()
        # Assert specific outputs
        self.assertIn("You had blackjack! It pays 3:2, which is 7.5 chips!", printed_output)
        self.assertIn("In total, you won 7.5 chips this round.", printed_output)
        self.assertIn("BANKROLL: 1007.5 chips", printed_output)

    def test_sp(self):
        with patch('builtins.input', side_effect=['10', 'n', 'n', 'sp']), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(1, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged")) 
            shoe.shoe[2] = (Card(1, "rigged")) #you have aces (after you split aces, you can't hit)
            shoe.shoe[3] = (Card(9, "rigged")) 
            shoe.shoe[4] = (Card(9, "rigged")) #first hand
            shoe.shoe[5] = (Card(10, "rigged")) #second hand is 21
            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()
        # Assert specific outputs
        with self.assertRaises(AssertionError): #success if it fails--the 21 after split should not be a blackjack
            self.assertIn("Total value: Blackjack!", printed_output)
        self.assertIn("Total value: 21", printed_output) #continuation of above; instead, it should be 21.

        self.assertIn("Push. You tied your first hand. You keep your wager of 10 chips.", printed_output)
        self.assertIn("You won your second hand. You win 10 chips.", printed_output)
        self.assertIn("In total, you won 10 chips this round.", printed_output)
        self.assertIn("BANKROLL: 1010.0 chips", printed_output)

    def test_broke(self): #what if you're broke
        with patch('builtins.input', side_effect=['10', 'n', 'st']) as mock_input, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(5, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(5, "rigged")) #player should be able to split, double if not broke (of course player is broke in this test)
            shoe.shoe[3] = (Card(7, "rigged"))
            player1 = Human("A", shoe)
            player1.bankroll = float(10) #broke so shouldn't be able to insure, split, double
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()
        # Verify input() prompts
        mock_input.assert_any_call("What would you like to do? [h] hit, or [st] stand. ") #should only be able to hit, and no prompt to double or split
        with self.assertRaises(AssertionError): #success if it fails--meaning should have no prompt to insurance if broke
            mock_input.assert_any_call("Do you want insurance? [y] yes, or [n] no. ")
        # Assert specific outputs
        self.assertIn("You lost your hand. You lose 10 chips.", printed_output)
        self.assertIn("In total, you lost 10 chips this round.", printed_output)
        self.assertIn("BANKROLL: 0.0 chips", printed_output)
    
    def test_broke2(self): #what if you're kinda broke, and you got past splitting but with 0 chips after
        with patch('builtins.input', side_effect=['10', 'n', 'n', 'sp', 'h', 'st', 'h' , 'st']) as mock_input, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(5, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(5, "rigged")) #player should be able to split
            shoe.shoe[3] = (Card(7, "rigged")) #dealer has 18 and stands after we plau
            shoe.shoe[4] = (Card(5, "rigged")) #first hand after sp
            shoe.shoe[5] = (Card(5, "rigged")) #second hand after sp
            shoe.shoe[6] = (Card(10, "rigged")) #first hand hit
            shoe.shoe[7] = (Card(5, "rigged")) #second hand hit

            player1 = Human("A", shoe)
            player1.bankroll = float(20) #should be able to split, but not double after split even though the 10 total should allow for splitting
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Verify input() prompts
        mock_input.assert_any_call("What would you like to do? [h] hit, or [st] stand. ")
        mock_input.assert_any_call("Do you want insurance? [y] yes, or [n] no. ")
        with self.assertRaises(AssertionError): #if this fails--meaning no prompt to double since we're broke after splitting
            mock_input.assert_any_call("What would you like to do? [h] hit, [d] double down, or [st] stand. ")
        # Assert specific outputs
        self.assertIn("You won your first hand. You win 10 chips.", printed_output)
        self.assertIn("You lost your second hand. You lose 10 chips.", printed_output)
        self.assertIn("In total, you won and lost no chips this round.", printed_output)
        self.assertIn("BANKROLL: 20.0 chips", printed_output)

    def test_double(self): #does double subtract money correctly
        with patch('builtins.input', side_effect=['10', 'n', 'n', 'd']) as mock_input, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(5, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(6, "rigged")) #player has 11, basic strategy says always double
            shoe.shoe[3] = (Card(7, "rigged")) #dealer has 18 and stands after we play
            shoe.shoe[4] = (Card(2, "rigged")) #we get a 2 :( for a total of 13. 

            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Verify input() prompts
        mock_input.assert_any_call("Do you want insurance? [y] yes, or [n] no. ")
        # Assert specific outputs
        self.assertIn("You lost your hand. You lose 20 chips.", printed_output)
        self.assertIn("In total, you lost 20 chips this round.", printed_output)
        self.assertIn("BANKROLL: 980.0 chips", printed_output)
    
    def test_insure_surrender(self): #what if you lose insurance and then surrender?
        with patch('builtins.input', side_effect=['10', 'y', 'y']) as mock_input, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect='5'):
                shoe = Shoe(1)
            shoe.shoe[0] = (Card(10, "rigged"))
            shoe.shoe[1] = (Card(1, "rigged"))
            shoe.shoe[2] = (Card(6, "rigged")) #player has 16, basic strategy says surrender against dealer ace
            shoe.shoe[3] = (Card(7, "rigged")) #dealer has 18 and stands after we play

            player1 = Human("A", shoe)
            dealer1 = Dealer(shoe)
            # Run the game round
            game_round(player1, dealer1, shoe)
            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Verify input() prompts
        mock_input.assert_any_call("Do you want insurance? [y] yes, or [n] no. ")
        # Assert specific outputs
        self.assertIn("You had surrendered your hand and forfeited half of your original wager, which calculates to a loss of 5.0 chips.", printed_output)
        self.assertIn("In total, you lost 10.0 chips this round.", printed_output)
        self.assertIn("BANKROLL: 990.0 chips", printed_output)
    
    def test_play(self): #to test play the game myself with rigged inputs
        if True:
            return
        with patch('builtins.input', side_effect='5'):
            shoe = Shoe(1)
        shoe.shoe[0] = (Card(10, "rigged"))
        shoe.shoe[1] = (Card(1, "rigged"))
        shoe.shoe[2] = (Card(6, "rigged")) #player has 16, basic strategy says surrender against dealer ace
        shoe.shoe[3] = (Card(7, "rigged"))
        player1 = Human("A", shoe)
        player1.bankroll = float(30)
        dealer1 = Dealer(shoe)
        game_round(player1, dealer1, shoe)

if __name__ == "__main__":
    unittest.main()