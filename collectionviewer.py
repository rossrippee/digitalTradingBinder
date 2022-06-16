import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
from kivy.uix.button import Button            # This lets us dynamically create buttons, which will be used in our popup if the user wants to make a new collection
from kivy.uix.gridlayout import GridLayout    # This lets us create a grid that will bind other objects together
import sqlite3                                # This is for python's built-in database manager
import cardadder                              # This defines the card adder screen
import digimoncard                            # This defines the visual representation of a digimon card

class CollectionViewer(Screen):
    """This defines the functionality of the collections screen, which will let the user view/edit their existing collections, add a new collection, or go back to the dashboard"""
    # This ObjectProperty will allow us to add buttons representing collections to the user's dashboard based on their own personal collections
    collectionContainer = ObjectProperty(None)
    collectionFilter = ObjectProperty(None)
    instructions = ObjectProperty(None)
    # This will let us keep track of the user's username during their session
    username = None
    # This will store the list of cards owned by the user so we only have to fetch the list one time (unless the list is changed, then it must be refreshed)
    cardList = None
    gameName = None
    listSize = 0
    def addCards(self):
        """If the user successfully logs in, this function will make a dashboard screen and switch the display to that screen, passing in the account's username"""
        # This adds a collections screen to the screen manager
        cardAdder = cardadder.CardAdder(name='card_adder')
        # This passes the account's username to the collections screen
        cardAdder.setUsername(self.username)
        cardAdder.setGame(self.gameName)
        cardAdder.setParentCollection(self)
        # This adds the dashboard display screen to the screen manager's screens
        self.manager.add_widget(cardAdder)
        # This switches the screen to the new dashboard screen
        self.manager.current = 'card_adder'
    
    def backToCollections(self):
        """If the user presses the Go back to the dashboard button, this function will switch the display back to the dashboard screen and delete the collections screen"""
        # Clear everything before leaving just to be safe
        self.username = None
        # This switches the screen back to the collections
        self.manager.current = 'collections'
        # This gets rid of the collections screen
        self.manager.remove_widget(self)
        # This deletes this instance for efficiency
        del self
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CollectionsViewer()
    
    def setGame(self, gameName):
        self.gameName = gameName
        self.viewAllCards()
    
    def setUsername(self, newUsername):
        """This is called whenever a user views their collection from the dashboard so that their personal collections can be loaded"""
        self.username = newUsername

    def viewAllCards(self):
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Grab the collections associated with the given username, and sort them based on most-recently-used
        cursor.execute('SELECT cardname, cardset, quantity FROM userCards WHERE username="%s" AND game="%s" ORDER BY cardname ASC' % (self.username, self.gameName))
        # Grab the results of the query and store them in gameList
        self.gameList = cursor.fetchall()
        self.listSize = cursor.execute("SELECT COUNT(*) FROM userCards").fetchone()[0]
        # Close the connection
        connection.close()
        self.cardContainer.clear_widgets()
        cardContainer = GridLayout(cols=1, spacing=50, size_hint_y=None)
        if self.listSize < 20:
            numToShow = self.listSize
        else:
            numToShow = 20
        for i in range(numToShow):
            newCard = digimoncard.DigimonCard()
            newCard.setName(self.gameList[i][0], self)
            newCard.setCardNumber(self.gameList[i][1])
            newCard.setQuantity(self.gameList[i][2])
            cardContainer.add_widget(newCard)
        cardContainer.height = 40 * (numToShow + 12)
        self.cardContainer.add_widget(cardContainer)