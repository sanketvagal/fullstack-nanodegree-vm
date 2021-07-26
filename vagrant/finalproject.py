from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


#ADD JSON API ENDPOINT HERE

@app.route('/restaurants/JSON/')
def restaurantJSON():
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	MenuItems=[i.serialize for i in items]
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)


#RESTAURANTS CODE


@app.route('/restaurants/')
def showRestaurants():
	#return "this page will show all restaurants"
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
	#return "this page will be for making new restaurants"
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash("new restaurant created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	#return "this page will be for editing restaurant %s" %restaurant_id
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("restaurant name edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = editedRestaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	deleteRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		session.commit()
		#flash("restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html',  restaurant=deleteRestaurant)


#RESTAURANT MENU CODE



@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	#print items.first()
	if items.first() != None:
		return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id)
	else:
		return render_template('emptymenu.html', restaurant=restaurant)



@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	if request.method == 'POST':
		#newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		newItem = MenuItem(name = request.form['name'], 
			description = request.form['description'], 
			price = request.form['price'], 
			course = request.form['course'], 
			restaurant_id = restaurant_id)
		#print request.form['course']
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)




@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
			#editedItem.description = request.form['name']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash("menu item edited!")

		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
	


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one() 
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("menu item deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete)





if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)


