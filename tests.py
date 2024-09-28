import unittest
from blackjack import *

class CreateTests(unittest.TestCase):
    def test_deck_length(self): #basic test to utilize unittest
        self.assertEqual(len(create_deck(6)), 52 * 6)

    def test_deck(self): #tests if deck will self shuffle after using every card
        list = []
        for i in range(0, 52 * 6):
            deck_deal(list)
        temp = deck_deal(list)
        print("deal after shuffle above.")
        print("card: " + str(temp.value))
        self.assertEqual(temp in list, True)
        
    def test_count(self): #1+1+13=1+1+10=12
        obj = Hand("test")
        obj.rig(1)
        obj.rig(1)
        obj.rig(13)
        self.assertEqual(obj.count(), 12)
    
    def test_count2(self): #1+1+1+8=11+11+11+8-10-10=21
        obj = Hand("test")
        obj.rig(1)
        obj.rig(1)
        obj.rig(1)
        obj.rig(8)
        self.assertEqual(obj.count(), 21)

    def test_display_count(self): #see if natural blackjack has custom total count
        obj = Hand("test")
        obj.rig(1)
        obj.rig(11)
        self.assertEqual("Blackjack!", obj.display_count())


if __name__ == "__main__":
    unittest.main()
