# Imports the Card class, which ViewOnlyCard inherits from
from card import Card

class AddableCard(Card):
    """This defines the functionality of the "addable card", which will represent a card in the game that the user can add a given quantity of to their collection"""

    def addCards(self):
        """If the user clicks the + button on an addable card, the adder that hosts the card will update the user's collection with the card's info and quantity provided"""
        self.adder.updateCollection(self.name.text, self.cardnumber.text, self.quantity.text)
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return AddableCard()
    
    def decreaseQuantity(self):
        """This allows the user to decrease the quantity of this card that would be added to their collection"""
        if int(self.quantity.text) > 1:
            self.quantity.text = str(int(self.quantity.text) - 1)
    
    def increaseQuantity(self):
        """This allows the user to increase the quantity of this card that would be added to their collection"""
        self.quantity.text = str(int(self.quantity.text) + 1)