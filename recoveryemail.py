# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen     # This lets us more easily manage a "super-screen" that contains all the other possible screens (log in, create account, etc.)
# Python Built-in Imports
import sqlite3                                # This is for python's built-in database manager

class RecoveryEmailDisplay(Screen):
    """This defines the functionality of the recovery email screen, which will let the user enter a username and password to attempt to create a new account or give
    them the option to go back to the log in screen instead"""
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the RecoveryEmailDisplay definition
    email = ObjectProperty(None)
    instructions = ObjectProperty(None)
    username = ObjectProperty(None)
    # This ReturnReference will let us make references to the log in screen that created us
    ReturnReference = None
    
    def attemptSendRecoveryEmail(self):
        """This is the code that will execute if someone presses the 'Create account' button on the create account screen"""
        # Grab the username and password typed into the text field
        givenUsername, givenEmail = self.username.text, self.email.text
        # Make sure the user actually supplied a username
        if len(givenUsername) == 0:
            # Change the instructions label to let the user know they didn't enter a username
            self.instructions.text = '''Please enter the username of the account that you forgot the password to!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Make sure the user actually supplied an email
        if len(givenEmail) == 0:
            # Change the instructions label to let the user know they didn't enter an email
            self.instructions.text = '''Please enter the email address of the account that you forgot the password to!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Connect to the database
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Make sure there is no account that already exists with the given username
        cursor.execute('SELECT email FROM accounts WHERE username="%s"' % givenUsername)
        # Grab the results of the query
        result = cursor.fetchall()
        # If there are no records, that means the given username does not exist. Let the user know!
        if len(result) == 0:
            self.instructions.text = '''Recovery attempt failed!
Either the given username has a typo or the given email address was incorrect!
Please try again!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # If there is a record, check if the given email matches the expected email. If so, send the user an account recovery email (to be implemented in the future)
        elif result[0][0] == str(givenEmail):
            # For now, pretend the user was sent an account recovery email
            self.ReturnReference.successfullySentRecoveryEmail()
            self.backToLogInScreen()
        # This means the given email did not match the expected email. Let the user know that either the given username does not exist (keeping it ambiguous to protect against hackers) or the email was wrong
        else:
            self.instructions.text = '''Recovery attempt failed!
Either the given username has a typo or the given email address was incorrect!
Please try again!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # Close the connection
        connection.close()
    
    def backToLogInScreen(self):
        """If the user presses the Back to Log In button, this function will switch the display back to the log in screen and delete the create account screen"""
        # It feels more natural to clear the input text before leaving so there is no input text when the user returns to this screen
        self.username.text = ''
        self.email.text = ''
        # This switches the screen back to the log in screen
        self.manager.current = 'log_in'
        # This gets rid of the recovery email screen
        self.manager.remove_widget(self)
        # This deletes the recovery email display to save memory
        del self
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CreateAccountDisplay()
    
    def setInstructionsColor(self, r, g, b):
        """This will change the color of the instructions label to catch the user's attention and let them know something's wrong"""
        self.instructions.color = r, g, b, 1
        
    def setReturnReference(self, returnReference):
        """This will set a reference to the log in screen that created us"""
        self.ReturnReference = returnReference