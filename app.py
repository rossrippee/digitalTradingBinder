# Importing external libraries
import kivy                                         # The kivy library is not built into python
from kivy.app import App                            # The foundation of a kivy app
from kivy.uix.screenmanager import ScreenManager    # This lets you more easily manage the multiple possible screens (log in, create account, etc.)
import sqlite3                                      # This is for python's built-in database manager
import login                                        # This defines the log in screen
import createaccount                                # This defines the create account screen
import recoveryemail                                # This defines the recovery email screen (forgot my password)
import dashboard

class MyApp(App):
    """This is going to contain the code for the app"""
    def build(self):
        """The build method is automatically recognized by kivy as the definition for what the app should display"""
        # Create a new database or connect to one
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Create a table for the users if one does not already exist. It simply contains a username column and a password column, where the username is a primary key
        cursor.execute("""
            CREATE TABLE if not exists accounts(username text PRIMARY KEY, password text, email text)
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