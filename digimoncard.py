# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager

class DigimonCard(Screen):
    """This defines the functionality of the collections screen, which will let the user view/edit their existing collections, add a new collection, or go back to the dashboard"""
    # These ObjectProperties will allow us to add buttons representing collections to the user's dashboard based on their own personal collections
    cardnumber = ObjectProperty(None)
    name = ObjectProperty(None)
    quantity = ObjectProperty(None)
    # This references the card adder screen that hosts this digimon card
    adder = None

    def addCards(self):
        """If the user successfully logs in, this function will make a dashboard screen and switch the display to that screen, passing in the account's username"""
        self.adder.updateCollection(self.name.text, self.cardnumber.text, self.quantity.text)
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CardAdder()
    
    def decreaseQuantity(self):
        """This allows the user to decrease the quantity of this card that would be added to their collection"""
        if int(self.quantity.text) > 1:
            self.quantity.text = str(int(self.quantity.text) - 1)
    
    def increaseQuantity(self):
        """This allows the user to increase the quantity of this card that would be added to their collection"""
        self.quantity.text = str(int(self.quantity.text) + 1)
        
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