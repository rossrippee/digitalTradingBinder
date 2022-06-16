# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.boxlayout import BoxLayout      # The DigimonCard is a BoxLayout containing objects that display the information that represents it

class Card(BoxLayout):
    """This defines the functionality of the card, which is a visual representation of a card. This is a parent class to "viewonlycard" and "addablecard"."""
    # These ObjectProperties will allow us to store information about a card
    cardnumber = ObjectProperty(None)
    name = ObjectProperty(None)
    quantity = ObjectProperty(None)
    # This references the card adder screen that hosts this card
    adder = None

    def setQuantity(self, quantity):
        """This allows the user to type in the quantity of this card that would be added to their collection"""
        self.quantity.text = str(quantity)
    
    def setCardNumber(self, newCardNumber):
        """This is called to change this card's displayed card number to match the card this represents"""
        self.cardnumber.text = newCardNumber
    
    def setName(self, newName, newAdder):
        """This is called to change this card's displayed name to match the card this represents"""
        self.name.text = newName
        self.adder = newAdder