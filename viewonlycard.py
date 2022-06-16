# Imports the Card class, which ViewOnlyCard inherits from
from card import Card

class ViewOnlyCard(Card):
    """This defines the functionality of the "view only card", which will represent a card in the user's collection without letting them change the quantity"""

    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return ViewOnlyDigimonCard()