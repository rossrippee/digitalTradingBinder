# Importing external libraries
import kivy                           # The kivy library is not built into python
from kivy.app import App              # The foundation of a kivy app
from kivy.uix.widget import Widget    # This allows a kv file to fill in a "super" widget

class InitialDisplay(Widget):
    pass

class MyApp(App):
    """This is going to contain the code for the app"""
    def build(self):
        """The build method is automatically recognized by kivy as the definition for what the app should display"""
        # Tell the app to build the display based on the contents of my.kv
        return InitialDisplay()
    
# If this module is the one that was initially selected to run, it will call the MyApp method to start the app
if __name__ == "__main__":
    # Runs the app as defined by the class MyApp
    MyApp().run()