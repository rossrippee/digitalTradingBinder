# Kivy Imports
import kivy                                         # The kivy library is not built into python
from kivy.app import App                            # The foundation of a kivy app
from kivy.uix.screenmanager import ScreenManager    # This lets you more easily manage the multiple possible screens (log in, create account, etc.)
# Python Built-in Imports
import sqlite3                                      # This is for python's built-in database manager
# Internal Module Imports
import login                                        # This defines the log in screen

class MyApp(App):
    """This is going to contain the code for the app"""
    def build(self):
        """The build method is automatically recognized by kivy as the definition for what the app should display"""
        # Create a new database or connect to one
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Create a table for the users if one does not already exist. It contains username, password, and email columns, where the username is a primary key
        cursor.execute("""
            CREATE TABLE if not exists accounts(username text PRIMARY KEY, password text, email text)
        """)
        # Commit this execution to the database
        connection.commit()
        # Create a table for the users' collections if one does not already exist. It contains id, game, and username, and lastUsed columns, where the id is an auto-incremented primary key, the game is the name of the game that the collection of cards belongs to, the username is a foreign key referencing which user owns the collection, and the lastUsed is a way of sorting the collections by last used for user convenience
        cursor.execute("""
            CREATE TABLE if not exists userCollections(ID INTEGER PRIMARY KEY AUTOINCREMENT, game text, username text, lastUsed DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(username) REFERENCES accounts(username))
        """)
        # Commit this execution to the database
        connection.commit()
        # Create a table for the users' collections if one does not already exist. It contains id, game, and username, and lastUsed columns, where the id is an auto-incremented primary key, the game is the name of the game that the collection of cards belongs to, the username is a foreign key referencing which user owns the collection, and the lastUsed is a way of sorting the collections by last used for user convenience
        cursor.execute("""
            CREATE TABLE if not exists userCards(ID INTEGER PRIMARY KEY AUTOINCREMENT, game text, username text, cardname text, cardset text, quantity INTEGER, FOREIGN KEY(username) REFERENCES accounts(username))
        """)
        # Commit this execution to the database
        connection.commit()
        # Close this connection
        connection.close()
        # Make a screen manager
        sm = ScreenManager()
        # Add the log in screen as the first screen
        sm.add_widget(login.LogInDisplay(name='log_in'))
        # The display will render the log in screen before anything else
        return sm
    
# This creates a new instance of MyApp and calls its run method, which has the effect of running this app
MyApp().run()