# Digital Trading Binder
## What is this?
### This is my first kivy project and my first major personal project since graduating
Post-graduation (May 7th), I have made it my goal to learn python since I did not take electives at my university that taught the language. After using many tutorials to learn the fundamentals, I decided to think of a fun project to practice my new skills.

### My idea:
I am a big fan of trading card games, and have been playing them since I've known how to read. I grew up playing Yu-Gi-Oh! with my two brothers. I attend my local game store's events for playing my favorite card games with my local community. A common occurrence is for people to try to trade for the cards they're missing in their collections (after all, they're trading card games!!). Trading usually starts in one of two ways:

* Do you have any copies of X?
* Can I look through your trading binder?

There are some major issues with the traditional system of trading. Card collectors usually have hundreds, if not thousands, of cards in their collections! If they are asked if they have a specific card, they have to think hard about whether or not they do. It's easy to lose track of what all you have when you have so much. It is also possible that they will misremember because they had a copy and either lost it, already traded it, or sold it but forgot that they did. On the other hand, simply looking through a trading binder will not be the best solution, because no binder is big enough to carry a collector's entire collection. They may not have the card in that binder, but they could have it at home.

I would like to have an app that makes trading into an easier process. This requires the ability to save your collection to your own username, and having the ability to search through the colleciton under someone else's username. Part of making it an easier process would be having a method of filtering through the collections to try to find a specific card or a card that fits into a given category. For example:

Say my Digimon Trading Card collection contains...

* MameTyramon, BT7-049
* Lucemon, BT4-115
* Pulsemon, BT6-033
* Jokermon, BT5-078

If my friend wants to know if I have Lucemon, rather than having to visually scan my collection, they should be able to search for "Lucemon" and see the copies that I own. As another example, if my friend wants to know what digimon cards I have from the latest set (BT7), they should be able to add a filter for the BT7 and see that I have MameTyramon.

Additionally, I would like to give the users a "wishlist" feature, where a user could come up with a list of the cards they do not have and would like to trade for. That way, whenever they look at another user's collection, they can simply check whether or not someone's collection contains any of the cards in their wishlist. I would also like to have a "trading group" feature, where users can invite other users to a trading group. This would let you check your friends' collections without having to search their usernames each time. Also, whenever a user in that group updates their collection, it should send a notification to the other users in that group that someone in their trading group obtained a card if it's in their wishlist.

### The "how"
Since I want this to be an opportunity to hone my skills developing an application using python, I will be using the kivy library for this project. Kivy is used to define what will be on the phone screen. It is implemented in python and meant to be used with python. I am also temporarily using sqlite3, python's built-in serverless database engine. I will transition to an SQL database hosted on a server when I'm ready to deploy the application and share it with my friends at my local game store.

## What is there now?
* A 'log in' screen, 'create account' screen, and 'forgot password' screen for associating your collection with a username
* A 'dashboard' screen where you interact with the app. Currently, it only gives you the option of viewing/editing your collection
* A 'collections' screen that displays the different collections you currently have stored (for conveniently separating your cards based on which game they're from). It also gives you the option of adding a new collection. The collections can be tapped to view or edit the cards stored in them
* A 'collection viewer' screen that displays the cards stored in your selected collection. It can be searched through or filtered by set. There is also a button for adding cards (to be implemented)

## Known issues
* The account creation screen isn't good at detecting whether or not a fake email address has been given. The regular expression needs tweaking

## Testing
Currently testing is conducted manually since the stage of development is just setting up the infrastructure instead of focusing on features

## How to use
This mobile application currently has two dependencies:
* Python
* Kivy

To install python, use the official website: https://www.python.org/downloads/

After installing python, install kivy from the command line using the command:

python -m pip install kivy[full]

Note that this command may require extra privileges, which can be achieved by running the command prompt as an administrator on Windows operating systems or using sudo on Linux operating systems.

Having installed the required dependencies, clone this repository to your local machine.

git clone https://github.com/rossrippee/digitalTradingBinder/

Then, in the directory where you cloned this repository, issue the command

python app.py

As mentioned earlier, this project uses sqlite3, which is not connected to a server! This application is currently purely local to your machine. Therefore it is perfectly safe to make an account with a fake email and start exploring the application!

## Sources used during development (so far)
* Tech With Tim (YouTube channel) Kivy Tutorials Python (Playlist): (https://www.youtube.com/watch?v=bMHK6NDVlCM&list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn)
* Codemy.com (YouTube channel) Using SQLite3 Database With Kivy - Python Kivy GUI Tutorial #55 (video): (https://www.youtube.com/watch?v=X2MkC1ru3cQ)
