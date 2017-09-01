from database import Database
from menu import Menu

__author__ = 'neehad' #this is used for importing purposes to match
Database.initialize() #make an instance of the database

menu = Menu() #make a new menu object
menu.run_menu() #use the run menu method 
