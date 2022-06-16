# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.uix.button import Button            # This lets us dynamically create buttons, which will be used in our popup if the user wants to make a new collection
from kivy.uix.gridlayout import GridLayout    # This lets us create a grid that will bind other objects together (horizontally and vertically)
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.popup import Popup              # This lets us dynamically create a popup, which will be made if the user wants to make a new collection so they can specify which game the collection is for
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
from kivy.uix.scrollview import ScrollView    # This lets us create a scrollable view that will contain a list of digimon card objects
# Python Built-in Imports
import json                                   # This is for python's built-in json manager
import re                                     # This is for python's built-in regular expression manager
import sqlite3                                # This is for python's built-in database manager
# External Module Imports
from natsort import natsorted                 # This method is for sorting strings in a way that puts 'BT10' after 'BT9' instead of after 'BT1'
# Internal Module Imports
import addablecard                            # This defines the visual representation of the addable version of a card

class CardAdder(Screen):
    """This defines the functionality of the collections screen, which will let the user view/edit their existing collections, add a new collection, or go back to the dashboard"""
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the CardAdder definition
    collectionContainer = ObjectProperty(None)
    collectionFilter = ObjectProperty(None)
    instructions = ObjectProperty(None)
    # This will store the list of cards owned by the user so we only have to fetch the list one time (unless the list is changed, then it must be refreshed)
    cardList = None
    # This will let us keep track of the name of the game that we are adding cards for in the database
    gameName = None
    # This will let us keep track of the user's collection that we are adding to
    parentCollection = None
    # This will let us keep track of the user's username during their session
    username = None
    # These booleans will help keep track of whether or not certain steps are necessary during a method's execution
    filtersApplied = False
    initialLoad = True
    
    def backToCollection(self):
        """If the user presses the "Go back to your collection" button, this function will switch the display back to the collectionviewer screen and delete the cardadder screen"""
        # This makes the collection viewer reload the collection in case new cards have just been added
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
        """This generates a popup containing a button for each of the sets the cards are from. If the user selects one of the sets, the cards they can add are filtered to only the ones from that set unless the user clears the filter"""
        # Make a new set for the card sets to guarantee the card set names are unique
        setSet = set()
        # Grab all the card sets from the card numbers, which appear to the left of the '-'
        for i in range(len(self.cardList)):
            setSet.add(self.cardList[i]['cardnumber'].split('-')[0])
        # Now that we have a set of unique card sets, convert it to a list because it's easier to sort
        setList = list(setSet)
        # Using natsort, the card sets are sorted such that 'BT10' comes after 'BT9' instead of 'BT1' (alphabetically sorted but numeric characters are treated as numbers)
        sortedSetList = natsorted(setList)
        # This creates a new popup that contains a scroll view, centered and taking up 64% of the screen
        popup = Popup(title='Choose a set',
            content=ScrollView(do_scroll_x=False, do_scroll_y=True),
            size_hint=(.8, .8))
        # This creates a grid layout which will contain all the card set names as buttons
        cardContainer = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # For each card set name, add a button to the grid layout representing it
        for i in range(len(sortedSetList)):
            # The button's text should be the card set name that it represents
            btn = Button(text=sortedSetList[i], height=40, size_hint_y=None)
            # If the user presses this button, filterBySet will be called with the card set name
            btn.bind(on_release = lambda btn: self.filterBySet(btn.text, popup))
            # Finally, the button is added to the grid layout
            cardContainer.add_widget(btn)
        # Finally, add a button at the bottom in case the user decides they don't want to filter by set after all
        btn = Button(text="Never mind", height=40, size_hint_y=None)
        btn.bind(on_release = lambda btn: popup.dismiss())
        cardContainer.add_widget(btn)
        # Set the height of the grid layout so that the scroll view knows how much there is to scroll through when it is added
        cardContainer.height = 40 * (len(sortedSetList) + 1) + 10 * len(sortedSetList)
        # The grid layout full of buttons is added to the scroll view
        popup.content.add_widget(cardContainer)
        # Now that this popup has been built, it can be displayed to the user
        popup.open()
        
    def clearFilters(self):
        """This cancels any of the filters that the user applied"""
        # Remove the text from the text box (if any) to avoid confusion for the user
        self.collectionFilter.text = ''
        # In case there were no filters applied to begin with, avoid rebuilding the list if unnecessary
        if self.filtersApplied == False:
            return
        # If there were filteres applied, rebuild the list with no filters
        self.viewAllCards()
        
    def fillCardCollection(self, cardList):
        """This fills the scroll view with a grid layout containing the cards that the user can add to their collection"""
        # Get rid of the grid layout already available in the card container
        self.cardContainer.clear_widgets()
        # This creates a grid layout which will contain all the card set names as buttons
        cardContainer = GridLayout(cols=1, spacing=50, size_hint_y=None)
        # To avoid loading potentially thousands of cards at once, only the first 20 cards are loaded for speed and memory efficiency
        if len(cardList) < 20:
            numToShow = len(cardList)
        else:
            numToShow = 20
        # Make an AddableCard to represent the cards that can be added by the user
        for i in range(numToShow):
            newCard = addablecard.AddableCard()
            newCard.setName(cardList[i]['name'], self)
            newCard.setCardNumber(cardList[i]['cardnumber'])
            cardContainer.add_widget(newCard)
        # Set the height of the grid layout so that the scroll view knows how much there is to scroll through when it is added
        cardContainer.height = 40 * (numToShow + 24)
        # The grid layout full of buttons is added to the scroll view
        self.cardContainer.add_widget(cardContainer)
        
    def filterByName(self):
        """This filters the cards to only cards whose name contains the name entered by the user"""
        # This sets the flag that the user has applied a filter
        self.filtersApplied = True
        # Make a list to store the cards that apply towards the filter
        filteredCardList = []
        # Look at each card in the list and add it to our filtered card list if its name matches the filter
        for card in self.cardList:
            if re.search(self.collectionFilter.text, card['name'], re.IGNORECASE):
                filteredCardList.append(card)
        # Fill the cardCollection scroll view using this list
        self.fillCardCollection(filteredCardList)
    
    def filterBySet(self, chosenSet, popup):
        """This filters the cards to only cards whose cardnumber contains the set chosen by the user"""
        # This sets the flag that the user has applied a filter
        self.filtersApplied = True
        # Since the user chose a set from the popup, the popup is no longer necessary and can be dismissed
        popup.dismiss()
        # Make a list to store the cards that apply towards the filter
        filteredCardList = []
        # Look at each card in the list and add it to our filtered card list if its name matches the filter
        for card in self.cardList:
            if chosenSet in card['cardnumber']:
                filteredCardList.append(card)
        # Fill the cardCollection scroll view using this list
        self.fillCardCollection(filteredCardList)
        
    def plurality(self, amount):
        """This is used to determine whether a singular 'copy' should be printed or plural 'copies'"""
            if int(amount) == 1:
                return 'copy'
            else:
                return 'copies'
            
    def setGame(self, gameName):
        """This is called whenever a user makes a CardAdder so the game that cards should be added for will be known"""
        self.gameName = gameName
        # After storing the game that we are adding cards for, the cards from that game should be loaded for the user
        self.viewAllCards()
        
    def setParentCollection(self, parentCollection):
        """This is called whenever the user makes a CardAdder so the parent can be referenced later"""
        self.parentCollection = parentCollection
    
    def setUsername(self, newUsername):
        """This is called whenever the user makes a CardAdder so their account can be referenced later in interactions with the database"""
        self.username = newUsername
        
    def updateCollection(self, name, cardNumber, quantity):
        """This is called whenever the user clicks the '+' button on an AddableCard. It adds the card to the database, with the given quantity and associated with the adder's game and the user's username"""
        # Set up a connection to the database
        connection = sqlite3.connect('account_db.db')
        cursor = connection.cursor()
        # This query adds the card to the user's collection
        cursor.execute("INSERT INTO userCards(game, username, cardname, cardset, quantity) VALUES('%s', '%s', '%s', '%s', %d)" % (self.gameName, self.username, name, cardNumber, int(quantity)))
        # This actually runs the query
        connection.commit()
        # Close the database connection
        connection.close()
        # Change the instructions to let the user know the cards were added successfully
        self.instructions.text = 'Added %s %s of %s from %s' % (quantity, self.plurality(quantity), name, cardNumber.split('-')[0])
        
    def viewAllCards(self):
        """This adds all of the cards of the game associated with this CardAdder to the scroll view for the user"""
        # If this is being called by clearFilters, there's no need to reload the list of cards
        if self.initialLoad == True:
            # Get the cards from the json associated with the game that this CardAdder is associated with
            if self.gameName == 'Digimon TCG':
                digimonCardFile = open('digimoncards.json')
                # Store the list in cardList for future reference
                self.cardList = json.load(digimonCardFile)
            # For now, only the Digimon TCG has cards to add
            else:
                print("This game has no cards added yet, sorry!")
            # Change the flag to reflect the fact that we have already read the json for our card list
            self.initialLoad = False
        # Populate the scroll view with these cards
        self.fillCardCollection(self.cardList)