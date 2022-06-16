# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.uix.button import Button            # This lets us dynamically create buttons, which will be used in our popup if the user wants to make a new collection
from kivy.uix.gridlayout import GridLayout    # This lets us dynamically create a gridlayout, which is perfect because you cannot add things to an already-made popup, but you can add to the widgets inside of it
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.popup import Popup              # This lets us dynamically create a popup, which will be made if the user wants to make a new collection so they can specify which game the collection is for
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
# Python Built-in Imports
import sqlite3                                # This is for python's built-in database manager
# Internal Module Imports
import collectionviewer                       # This defines the collection viewer screen

class CollectionsDisplay(Screen):
    """This defines the functionality of the collections screen, which will let the user view/edit their existing collections, add a new collection, or go back to the dashboard"""
    # This ObjectProperty will allow us to add buttons representing collections to the user's dashboard based on their own personal collections
    collectionContainer = ObjectProperty(None)
    # This will let us keep track of the user's username during their session
    username = None
    # This will store the list of games in use by the user so we only have to fetch the list one time (unless the list is changed, then it must be refreshed)
    gameList = None
    gameName = None
    def backToDashboard(self):
        """If the user presses the Go back to the dashboard button, this function will switch the display back to the dashboard screen and delete the collections screen"""
        # Clear everything before leaving just to be safe
        self.username = None
        # This switches the screen back to the dashboard
        self.manager.current = 'dashboard'
        # This gets rid of the collections screen
        self.manager.remove_widget(self)
        # This deletes this instance for efficiency
        del self
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CollectionsDisplay()
    
    def buildButtons(self):
        """This is used to dynamically make buttons that link to the different games' collections in order of most-recently-used"""
        # Connect to the database
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Grab the collections associated with the given username, and sort them based on most-recently-used
        cursor.execute('SELECT game FROM userCollections WHERE username="%s" ORDER BY lastUsed DESC' % self.username)
        # Grab the results of the query and store them in gameList
        self.gameList = cursor.fetchall()
        # Build a button for each of the collections
        for i in range(len(self.gameList)):
            button = Button(text="%s" % self.gameList[i][0])
            button.bind(on_release = lambda button: self.openCollection(button.text))
            self.ids.collectionContainer.add_widget(button)
        # Close the connection
        connection.close()
        
    def chooseGame(self):
        """This makes a popup that gives the user options for which game their new collection should be for"""
        # This creates the popup with a title that lets the user know what it's for and it contains a gridlayout so we can easily add buttons to it
        popup = Popup(title='What game is this collection for?',
            content=GridLayout(cols=1),
            size_hint=(.8, .8))
        # This is a list of the most popular trading card games at my local game store
        buttonNamesList = ['Magic: The Gathering', 'Pokemon TCG', 'Yu-Gi-Oh!', 'Digimon TCG']
        # A list will be populated with the games that already have collections made for in the database
        usedGamesList = []
        for game in self.gameList:
            # The database retrieval has a list of lists, so we need to index twice to get the actual value
            usedGamesList.append(game[0])
        # Take the symmetric difference of the lists in their set representations so we don't give the user the option of making a collection for a game that they already have a collection for
        buttonNames = set(buttonNamesList).symmetric_difference(set(usedGamesList))
        # For what's left of the difference, make a button in the popup
        for name in buttonNames:
            # Make the size of the buttons scale based on how many there are
            btn = Button(text=name, size_hint_y=.8/len(buttonNames) + 1)
            # The buttons will call createCollection with their text values when they are pressed (and released)
            btn.bind(on_release = lambda btn: self.createCollection(btn.text, popup))
            # The buttons are added to the gridlayout that's in the popup
            popup.content.add_widget(btn)
        # Make a button for the case where the user decides not to make a new collection after all
        btn = Button(text='Never mind...', size_hint_y=.8/len(buttonNames) + 1)
        # This button will simply close the popup
        btn.bind(on_release = lambda btn: popup.dismiss())
        # Add this button to the gridlayout that's in the popup with the other buttons (if any)
        popup.content.add_widget(btn)
        # Now that this popup has been built, it can be displayed to the user
        popup.open()
        
    def createCollection(self, game, popup):
        """This function is called by a button in the popup. It will make a new collection for the given game and refresh the list of collections displayed. Then it will close the popup"""
        # Normal database stuff
        connection = sqlite3.connect('account_db.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO userCollections(game, username) VALUES('%s', '%s')" % (game, self.username))
        connection.commit()
        connection.close()
        # This will clear the existing list of collections
        self.ids.collectionContainer.clear_widgets()
        # This will rebuild it in the proper order with the new button on top
        self.buildButtons()
        # This closes the popup
        popup.dismiss()
        
    def openCollection(self, gameName):
        """If the user successfully logs in, this function will make a dashboard screen and switch the display to that screen, passing in the account's username"""
        # This adds a collections screen to the screen manager
        collectionsViewer = collectionsviewer.CollectionsViewer(name='collection_view')
        # This passes the account's username to the collections screen
        collectionsViewer.setUsername(self.username)
        collectionsViewer.setGame(gameName)
        # This adds the dashboard display screen to the screen manager's screens
        self.manager.add_widget(collectionsViewer)
        # This switches the screen to the new dashboard screen
        self.manager.current = 'collection_view'
        
    def setGame(self, gameName):
        """This is called whenever a user views their collection from the dashboard so that their personal collections can be loaded"""
        self.gameName = gameName
    
    def setUsername(self, newUsername):
        """This is called whenever a user views their collection from the dashboard so that their personal collections can be loaded"""
        self.username = newUsername
        self.buildButtons()