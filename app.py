# Importing external libraries
import kivy                                   # The kivy library is not built into python
from kivy.app import App                      # The foundation of a kivy app
from kivy.uix.widget import Widget            # This allows a kv file to fill in a "super" widget
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.button import Button            # This is strictly for testing purposes
import sqlite3                                # This is for python's database

class InitialDisplay(Widget):
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the InitialDisplay definition
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    instructions = ObjectProperty(None)
    
    def setInstructionsColor(self, r, g, b):
        """This will change the color of the instructions label to catch the user's attention and let them know something's wrong"""
        self.instructions.color = r, g, b, 1
    
    def attemptLogin(self):
        """This is the code that will execute if someone presses the 'Log in' button on the initial display"""
        # Grab the username and password typed into the text field
        givenUsername, givenPassword = self.username.text, self.password.text
        # Make sure the user actually supplied a username
        if len(givenUsername) == 0:
            # Change the instructions label to let the user know they didn't enter a username
            self.instructions.text = '''Please enter a username before trying to log in!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        if len(givenPassword) == 0:
            # Change the instructions label to let the user know they didn't enter a password
            self.instructions.text = '''Please enter a password before trying to log in!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Connect to the database
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Grab the password from the users table using the given username
        cursor.execute('SELECT password FROM users WHERE username="%s"' % givenUsername)
        # Grab the results of the query
        result = cursor.fetchall()
        # If there are no records, that means the supplied username is not a pre-existing account. Tell the user to create an account!
        if len(result) == 0:
            self.instructions.text = '''Log in attempt failed!
Either the given username does not exist yet or the given password was incorrect!
Please try again or create a new account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # If there is a record, check if the given password matches the expected password. If so, let the user move onto their account
        elif result[0] == givenPassword:
            pass
        # This means the given password did not match the expected password. Let them know that either the given username does not exist or the password was wrong
        else:
            pass
        # Close the connection
        connection.close()
    
    def newAccountScreen(self):
        """This is the code that will execute if someone presses the 'Create account' button on the initial display"""
        print('Time to make a new account!')
        #button = Button(text='Test button')
        #self.add_widget(button)
        
    def attemptAccountCreation(self):
        """This is the code that will put the new account in the database"""
        pass
        # Connect to the database
        #connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        #cursor = connection.cursor()
        # Grab the password from the users table using the given username
        #cursor.execute('SELECT password FROM users WHERE username="%s"' % self.username.text)
        # Grab the results of the query
        #result = cursor.fetchall()
        # If there are no records, that means the supplied username is not a pre-existing account. Tell the user to create an account!
        #if len(result) == 0:
            #self.instructions.text = '''Log in attempt failed!
#Either the given username does not exist yet or the given password was incorrect!
#Please try again or create a new account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            #self.instructions.color = 1, 0, 0, 1
        # If there is a record, check if the given password matches the expected password. If so, let the user move onto their account
        #elif result[0] == self.password.text:
            #pass
        # This means the given password did not match the expected password. Let them know that either the given username does not exist or the password was wrong
        #else:
            #pass
        # Close the connection
        #connection.close()

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
            CREATE TABLE if not exists users(username text PRIMARY KEY, password text)
        """)
        # Commit this execution to the database
        connection.commit()
        # Close this connection
        connection.close()
        # If the app has just been started, tell the app to build the display based on the InitialDisplay definition in my.kv as the initial display
        return InitialDisplay()
            
MyApp().run()