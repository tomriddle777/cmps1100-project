import unittest
from unittest.mock import patch, Mock
from io import StringIO

import blackjack #weird importing to lo

def lobotomize(seconds):
    return

blackjack.pause = lobotomize

from blackjack import *

class CreateTests(unittest.TestCase):
    """
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
    """
    def test_both_blackjack(self):
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
            game_round(player1, dealer1)

            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Assert specific outputs
        self.assertIn("Push. Both you and the dealer had blackjack. You keep your wager of 10 chips.\nIn total, you won 10.0 chips this round.", printed_output)

    def test_dealer_blackjack_insurance(self):
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
            game_round(player1, dealer1)

            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Assert specific outputs
        self.assertIn("In total, you won and lost no chips this round.", printed_output)

    def test__blackjack(self):
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
            game_round(player1, dealer1)

            # Get all printed outputs
            printed_output = mock_stdout.getvalue()

        # Assert specific outputs
        self.assertIn("In total, you won and lost no chips this round.", printed_output)

if __name__ == "__main__":
    unittest.main()