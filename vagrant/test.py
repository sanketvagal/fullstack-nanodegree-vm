from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, Menuitem
engine = create_engine('sqlite://restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheesepizza = Menuitem(name = "Cheese pizza", description = "Made with all natural ingredients and fresh mozarella", course = "Entree", price = "$8.99", restaurant = "myFirstRestaurant")