import kivy                                                 # The kivy library is not built into python
from kivy.properties import ObjectProperty                  # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen    # This lets us more easily manage a "super-screen" that contains all the other possible screens (log in, create account, etc.)
import sqlite3                                              # This is for python's built-in database manager
import re                                                   # This is for checking if the user gives a valid email string or not

class CreateAccountDisplay(Screen):
    """This defines the functionality of the create account screen, which will let the user enter a username and password to attempt to create a new account or give
    them the option to go back to the log in screen instead"""
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the InitialDisplay definition
    username = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    instructions = ObjectProperty(None)
    # This ReturnReference will let us make references to the log in screen that created us
    ReturnReference = None
    
    def attemptAccountCreation(self):
        """This is the code that will execute if someone presses the 'Create account' button on the create account screen"""
        # Grab the username and password typed into the text field
        givenUsername, givenEmail, givenPassword = self.username.text, self.email.text, self.password.text
        # Make sure the user actually supplied a username
        if len(givenUsername) == 0:
            # Change the instructions label to let the user know they didn't enter a username
            self.instructions.text = '''Please enter a username before trying to make an account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Make sure the user actually supplied an email
        if len(givenEmail) == 0:
            # Change the instructions label to let the user know they didn't enter an email
            self.instructions.text = '''Please enter an email before trying to make an account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Make sure the supplied email is of the format of an email
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, givenEmail)):
            # Change the instructions label to let the user know they didn't enter a valid email
            self.instructions.text = '''Please enter a real email before trying to make an account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        if len(givenPassword) == 0:
            # Change the instructions label to let the user know they didn't enter a password
            self.instructions.text = '''Please enter a password before trying to make an account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
            # Don't do anything else!
            return
        # Connect to the database
        connection = sqlite3.connect('account_db.db')
        # Create a cursor to be our middle-man with the connection
        cursor = connection.cursor()
        # Make sure there is no account that already exists with the given username
        cursor.execute('SELECT * FROM accounts WHERE username="%s"' % givenUsername)
        # Grab the results of the query
        result = cursor.fetchall()
        # If there are no records, that means the given username is available. Check if the email is already associated with another account
        if len(result) == 0:
            # Check if the given email is already in use
            cursor.execute('SELECT * FROM accounts WHERE email="%s"' % givenEmail)
            result = cursor.fetchall()
            # It is already in use, let them know and do not make the new account
            if len(result) > 0:
                self.instructions.text = '''Account creation failed!
The email provided is already being used by another account.
If you forgot the log in details for your old account, please click the Forgot your password button on the log in screen!'''
                self.setInstructionsColor(1, 0, 0)
            # It is not already in use, so make the new account
            else:
                cursor.execute("INSERT INTO accounts(username, password, email) VALUES('%s', '%s', '%s')" % (givenUsername, givenPassword, givenEmail))
                connection.commit()
                self.ReturnReference.successfulAccountCreation()
                self.backToLogInScreen()
        # This means the given username is already in use. Let them know and ask them to pick another username
        else:
            self.instructions.text = '''Account creation failed!
The given username is already in use!
Please try again with a different username!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # Close the connection
        connection.close()
    
    def backToLogInScreen(self):
        """If the user presses the Back to Log In button, this function will switch the display back to the log in screen and delete the create account screen"""
        # It feels more natural to clear the input text before leaving so there is no input text when the user returns to this screen
        self.username.text = ''
        self.email.text = ''
        self.password.text = ''
        # This switches the screen back to the log in screen
        self.manager.current = 'log_in'
        # This gets rid of the create account screen
        self.manager.remove_widget(self)
        # This deletes the create account display to save memory
        del self
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return CreateAccountDisplay()
    
    def setInstructionsColor(self, r, g, b):
        """This will change the color of the instructions label to catch the user's attention and let them know something's wrong"""
        self.instructions.color = r, g, b, 1
        
    def setReturnReference(self, returnReference):
        """This will set the ReturnReference instance to point to the log in screen that created this create account screen and will be returned to eventually"""
        self.ReturnReference = returnReference