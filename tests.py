import unittest
from unittest.mock import patch, Mock
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
        self.assertEqual(counting.running_count, 0)
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

if __name__ == "__main__":
    unittest.main()