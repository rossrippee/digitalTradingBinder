# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.uix.boxlayout import BoxLayout      # This lets us create a box that will bind other objects together (strictly horizontally)
from kivy.uix.button import Button            # This lets us dynamically create buttons, which will be used in our popup if the user wants to make a new collection
from kivy.uix.gridlayout import GridLayout    # This lets us create a grid that will bind other objects together (horizontally and vertically)
from kivy.uix.label import Label              # This lets us create a label to make things easier for the user to understand
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.popup import Popup              # This lets us dynamically create a popup, which will be made if the user wants to make a new collection so they can specify which game the collection is for
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
from kivy.uix.scrollview import ScrollView    # This lets us create a scrollable view that will contain a list of digimon card objects
from kivy.uix.textinput import TextInput      # This lets us create a text input object to let the user enter a number of digimon cards to add or type in the name of the card they want to add
# Python Built-in Imports
import json                                   # This is for python's built-in json manager
import re                                     # This is for python's built-in regular expression manager
import sqlite3                                # This is for python's built-in database manager
# External Module Imports
from natsort import natsorted                 # This method is for sorting strings in a way that puts 'BT10' after 'BT9' instead of after 'BT1'
# Internal Module Imports
import digimoncard                            # This defines the visual representation of a digimon card

class CardAdder(Screen):
    """This defines the functionality of the collections screen, which will let the user view/edit their existing collections, add a new collection, or go back to the dashboard"""
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the CardAdder definition
    collectionContainer = ObjectProperty(None)
    collectionFilter = ObjectProperty(None)
    instructions = ObjectProperty(None)
    # This will store the list of cards owned by the user so we only have to fetch the list one time (unless the list is changed, then it must be refreshed)
    cardList = None
    # This will let us keep track of the user's collection that we are adding to
    parentCollection = None
    # This will let us keep track of the user's username during their session
    username = None
    # These booleans will help keep track of whether or not certain steps are necessary during a method's execution
    filtersApplied = False
    initialLoad = True
    
    def backToCollection(self):
        """If the user presses the Go back to the dashboard button, this function will switch the display back to the dashboard screen and delete the collections screen"""
        self.parentCollection.viewAllCards()
        # Clear everything before leaving just to be safe
        self.username = None
        # This switches the screen back to the collections
        self.manager.current = 'collection_view'
        # This gets rid of the collections screen
        self.manager.remove_widget(self)
        # This deletes this instance for efficiency
        del self
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CardAdder()
        
    def chooseSet(self):
        setSet = set()
        for i in range(len(self.cardList)):
            setSet.add(self.cardList[i]['cardnumber'].split('-')[0])
        setList = list(setSet)
        print(setList)
        sortedSetList = natsorted(setList)
        popup = Popup(title='Choose a set',
            content=ScrollView(do_scroll_x=False, do_scroll_y=True),
            size_hint=(.8, .8))
        # For what's left of the difference, make a button in the popup
        cardContainer = GridLayout(cols=1, spacing=10, size_hint_y=None)
        for i in range(len(sortedSetList)):
            btn = Button(text=sortedSetList[i], height=40, size_hint_y=None)
            btn.bind(on_release = lambda btn: self.filterBySet(btn.text, popup))
            cardContainer.add_widget(btn)
        btn = Button(text=sortedSetList[i], height=40, size_hint_y=None)
        btn.bind(on_release = lambda btn: popup.dismiss())
        cardContainer.add_widget(btn)
        cardContainer.height = 40 * (len(sortedSetList) + 1) + 10 * len(sortedSetList)
        popup.content.add_widget(cardContainer)
        
        # Now that this popup has been built, it can be displayed to the user
        popup.open()
        
    def clearFilters(self):
        self.collectionFilter.text = ''
        if self.filtersApplied == False:
            return
        self.viewAllCards()
        
    def fillCardCollection(self, cardList):
        self.cardContainer.clear_widgets()
        cardContainer = GridLayout(cols=1, spacing=50, size_hint_y=None)
        if len(cardList) < 20:
            numToShow = len(cardList)
        else:
            numToShow = 20
        for i in range(numToShow):
            newCard = digimoncard.DigimonCard()
            newCard.setName(cardList[i]['name'], self)
            newCard.setCardNumber(cardList[i]['cardnumber'])
            cardContainer.add_widget(newCard)
        cardContainer.height = 40 * (numToShow + 24)
        self.cardContainer.add_widget(cardContainer)
        
    def filterByName(self):
        self.filtersApplied = True
        filteredCardList = []
        for card in self.cardList:
            if re.search(self.collectionFilter.text, card['name'], re.IGNORECASE):
                filteredCardList.append(card)
        cardContainer = GridLayout(cols=1, spacing=50, size_hint_y=None)
        if len(filteredCardList) < 20:
            numToShow = len(filteredCardList)
        self.fillCardCollection(filteredCardList)
    
    def filterBySet(self, chosenSet, popup):
        self.filtersApplied = True
        popup.dismiss()
        filteredCardList = []
        for card in self.cardList:
            if chosenSet in card['cardnumber']:
                filteredCardList.append(card)
        self.fillCardCollection(filteredCardList)
        
    def plurality(self, amount):
            if int(amount) == 1:
                return 'copy'
            else:
                return 'copies'
            
    def setGame(self, gameName):
        self.gameName = gameName
        
    def setParentCollection(self, parentCollection):
        self.parentCollection = parentCollection
    
    def setUsername(self, newUsername):
        """This is called whenever a user views their collection from the dashboard so that their personal collections can be loaded"""
        self.username = newUsername
        self.viewAllCards()
        
    def updateCollection(self, name, cardNumber, quantity):
        connection = sqlite3.connect('account_db.db')
        cursor = connection.cursor()
        print("INSERT INTO userCards(game, username, cardname, cardset, quantity) VALUES('%s', '%s', '%s', '%s', %d)" % (self.gameName, self.username, name, cardNumber, int(quantity)))
        cursor.execute("INSERT INTO userCards(game, username, cardname, cardset, quantity) VALUES('%s', '%s', '%s', '%s', %d)" % (self.gameName, self.username, name, cardNumber, int(quantity)))
        connection.commit()
        cursor.execute('SELECT cardname FROM userCards WHERE username="%s" AND game="%s" ORDER BY cardname ASC' % (self.username, self.gameName))
        # Grab the results of the query and store them in gameList
        gameList = cursor.fetchall()
        print(gameList[0][0])
        connection.close()
        self.instructions.text = 'Added %s %s of %s from %s' % (quantity, self.plurality(quantity), name, cardNumber.split('-')[0])
        
    def viewAllCards(self):
        if self.initialLoad == True:
            digimonCardFile = open('digimoncards.json')
            self.cardList = json.load(digimonCardFile)
            self.initialLoad = False
        self.fillCardCollection(self.cardList)