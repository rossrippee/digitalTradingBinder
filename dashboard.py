# Kivy Imports
import kivy                                   # The kivy library is not built into python
from kivy.properties import ObjectProperty    # This lets us access values defined in the kv file
from kivy.uix.screenmanager import Screen     # This lets us represent the possible displays as screens that can be held onto by a screen manager
# Python Built-in Imports
import login                                  # This defines the log in screen
# Internal Module Imports
import collectionsdisplay                     # This defines the collections display screen

class DashboardDisplay(Screen):
    """This defines the functionality of the dashboard screen, which will let the user view/edit their collection or log out"""
    # This ObjectProperty will allow us to look at the properties of the instructions object defined in the kv file under the DashboardDisplay definition
    instructions = ObjectProperty(None)
    # This will let us keep track of the user's username during their session
    username = None
    
    def build(self):
        """This is automatically called whenever the object is instantiated. It creates the display based on the definition found in the kv file and returns it"""
        return Dashboard()
    
    def logOut(self):
        """If the user presses the Log out button, this function will switch the display back to the log in screen and delete the dashboard screen"""
        # Clear everything before leaving just to be safe
        self.username = None
        self.instructions.text = 'Welcome username!'
        # Make a new log in screen and add it to the screen manager
        self.manager.add_widget(login.LogInDisplay(name='log_in'))
        # This switches the screen back to the log in screen
        self.manager.current = 'log_in'
        # This gets rid of the dashboard screen
        self.manager.remove_widget(self)
        # This deletes this instance for efficiency
        del self
        
    def newCollectionsScreen(self):
        """If the user successfully logs in, this function will make a dashboard screen and switch the display to that screen, passing in the account's username"""
        # This adds a collections screen to the screen manager
        collectionsDisplay = collectionsdisplay.CollectionsDisplay(name='collections')
        # This passes the account's username to the collections screen
        collectionsDisplay.setUsername(self.username)
        # This adds the dashboard display screen to the screen manager's screens
        self.manager.add_widget(collectionsDisplay)
        # This switches the screen to the new dashboard screen
        self.manager.current = 'collections'
    
    def setUsername(self, newUsername):
        """This is called whenever a user successfully logs in. The username used to log in is passed into this dashboard instance so we know who logged in.
        It saves the passed-in username to our username attribute so we can reference it later, and changes the instructions text to greet the user by their username"""
        self.username = newUsername
        self.instructions.text = '''Welcome %s!
This is your dashboard. From here you can view or edit your collections.
Whenever you're done, go ahead and log out!''' % self.username