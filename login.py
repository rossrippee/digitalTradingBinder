# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
# Python Built-in Imports
import sqlite3                                # This is for python's built-in database manager
# Internal Module Imports
import createaccount                          # This defines the create account screen
import dashboard                              # This defines the dashboard screen
import recoveryemail                          # This defines the recovery email screen (forgot my password)


class LogInDisplay(Screen):
    """This defines the functionality of the log in screen, which will let the user enter a username and password to attempt to login or give them the option to
    create a new account instead"""
    # These ObjectProperties will allow us to look at the properties of the objects defined in the kv file under the InitialDisplay definition
    instructions = ObjectProperty(None)
    password = ObjectProperty(None)
    username = ObjectProperty(None)
    
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
        # Grab the password from the accounts table using the given username
        loginString = 'SELECT password FROM accounts WHERE username="%s"' % givenUsername
        cursor.execute(loginString)
        # Grab the results of the query
        result = cursor.fetchall()
        # If there are no records, that means the supplied username is not a pre-existing account. Tell the user to create an account!
        if len(result) == 0:
            self.instructions.text = '''Log in attempt failed!
Either the given username does not exist yet or the given password was incorrect!
Please try again or create a new account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # If there is a record, check if the given password matches the expected password. If so, let the user move onto their account's dashboard
        elif result[0][0] == str(givenPassword):
            # Make a new dashboard screen, passing in the given username
            self.newDashboardScreen(givenUsername)
            # Remove the log in screen from the screen manager and delete this instance for efficiency
            self.manager.remove_widget(self)
            del self
        # This means the given password did not match the expected password. Let them know that either the given username does not exist or the password was wrong
        else:
            self.instructions.text = '''Log in attempt failed!
Either the given username does not exist yet or the given password was incorrect!
Please try again or create a new account!'''
            # This makes the text red, so hopefully that will catch the user's attention!
            self.setInstructionsColor(1, 0, 0)
        # Close the connection
        connection.close()
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return LogInDisplay()
    
    def newAccountScreen(self):
        """If the user presses the Create Account button, this function will make a create account screen and switch the display to that screen"""
        # It feels more natural to clear the input text before leaving so there is no input text when the user returns to the log in screen
        self.username.text = ''
        self.password.text = ''
        # This adds a create account screen to the screen manager
        createAccountDisplay = createaccount.CreateAccountDisplay(name='create_account')
        createAccountDisplay.setReturnReference(self)    # This allows you to change the instructions of the log in screen based on interactions on the new screen
        self.manager.add_widget(createAccountDisplay)
        # This switches the screen to the new create account screen
        self.manager.current = 'create_account'
        
    def newDashboardScreen(self, username):
        """If the user successfully logs in, this function will make a dashboard screen and switch the display to that screen, passing in the account's username"""
        # It feels more natural to clear the input text before leaving so there is no input text when the user returns to the log in screen
        self.username.text = ''
        self.password.text = ''
        # This adds a dashboard screen to the screen manager
        dashboardDisplay = dashboard.DashboardDisplay(name='dashboard')
        # This passes the account's username to the dashboard screen
        dashboardDisplay.setUsername(username)
        # This adds the dashboard display screen to the screen manager's screens
        self.manager.add_widget(dashboardDisplay)
        # This switches the screen to the new dashboard screen
        self.manager.current = 'dashboard'
        
    def newRecoveryEmailScreen(self):
        """If the user presses the Forgot your password button, this function will make a recovery email screen and switch the display to that screen"""
        # It feels more natural to clear the input text before leaving so there is no input text when the user returns to the log in screen
        self.username.text = ''
        self.password.text = ''
        # This adds a create account screen to the screen manager
        recoveryEmailDisplay = recoveryemail.RecoveryEmailDisplay(name='recovery_email')
        recoveryEmailDisplay.setReturnReference(self)    # This allows you to change the instructions of the log in screen based on interactions on the new screen
        self.manager.add_widget(recoveryEmailDisplay)
        # This switches the screen to the new create account screen
        self.manager.current = 'recovery_email'
        
    def setInstructionsColor(self, r, g, b):
        """This will change the color of the instructions label to catch the user's attention and let them know something's wrong"""
        self.instructions.color = r, g, b, 1
        
    def successfulAccountCreation(self):
        """This will change the instructions text to let you know that the account was made successfully"""
        self.instructions.text = '''Account created successfully!
Please log in with your new account.'''
        self.setInstructionsColor(0, 1, 0)
        
    def successfullySentRecoveryEmail(self):
        """This will change the instructions text to let you know that a recovery email was sent successfully"""
        self.instructions.text = '''Recovery email sent successfully!
Please check your email's inbox for the email and follow its instructions to reset your account's password.
If you don't see it, please check your spam folder!'''
        self.setInstructionsColor(0, 1, 0)