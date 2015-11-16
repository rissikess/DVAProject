from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
import logging
import sqlite3

logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
	conn = sqlite3.connect('yelp_data.db')
	cur = conn.cursor()
	tables_list = ['age', 'income_range', 'payment_types', 'ambience', 'meal_type', 'perks', 'dietary_restrictions', 'music', 'parking', "hours", "yelp"]
	fields = {}
	hours = ["000"]
	hours.extend(list(range(100, 1000, 100)))
	hours = ["0" + str(i) for i in hours]
	hours.extend(list(range(1000, 2500, 100)))
	for table in tables_list:
		cursor = cur.execute('select * from ' + table + ' limit 1')
		if(table == "yelp"):
			fields['General'] = {description[0].replace("_", " ").title():0 for description in cursor.description[1:]}
		elif(table == "hours"):
			fields['Hours'] = {}
		else:
			fields[table.replace("_", " ").title()] = [description[0].replace("_", " ").title() for description in cursor.description[1:]]

	# hour fields
	for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
		fields['Hours'][day + " open"] = hours
		fields['Hours'][day + " closed"] = hours

	#logger.debug(fields['Hours'])
	# general fields
	fields['General']['Price Range'] = [row[0] for row in cur.execute('SELECT DISTINCT price_range FROM yelp where price_range NOT NULL')]
	fields['General']['State'] = ['Arizona']
	del fields['General']['Block Id']
	del fields['General']['Latitude']
	del fields['General']['Longitude']
	del fields['General']['Type']
	del fields['General']['Neighborhoods']
	del fields['General']['Ages Allowed']
	del fields['General']['Open']
	del fields['General']['Full Address']
	del fields['General']['Name']

	fields['General']['City'] = ['Phoenix']
	fields['General']['Categories'] = ['Persian/Iranian', 'Cheesesteaks', 'Fondue', 'Food Court', 'Drugstores', 'Sandwiches', 'Chinese', 'Food Trucks', 'Ice Cream & Frozen Yogurt', 'Nightlife', 'Lounges', 'Shopping Centers', 'Hot Dogs', 'Real Estate', 'Buffets', 'Hotels', 'Vietnamese', 'Personal Chefs', 'Venues & Event Spaces', 'Hawaiian', 'Bubble Tea', 'Bakeries', 'Juice Bars & Smoothies', 'Wine Bars', 'Pubs', 'Thai', 'Tapas Bars', 'Shared Office Spaces', 'Pakistani', 'Spanish', 'Breweries', 'Food', 'Ethiopian', 'Steakhouses', 'Fruits & Veggies', 'Afghan', 'American (New)', 'Outlet Stores', 'Japanese', 'Middle Eastern', 'Ethnic Food', 'Health Markets', 'Indonesian', 'Sports Bars', 'Restaurants', 'Belgian', 'Sushi Bars', 'Gay Bars', 'Filipino', 'Beer, Wine & Spirits', 'Cocktail Bars', 'Live/Raw Food', 'Chocolatiers & Shops', 'Tapas/Small Plates', 'Cantonese', 'Food Stands', 'German', 'Delis', 'Arcades', 'Specialty Food', 'Greek', 'Salad', 'Brazilian', 'Fast Food', 'Cajun/Creole', 'Performing Arts', 'Donuts', 'Salvadoran', 'Desserts', 'Party & Event Planning', 'Herbs & Spices', 'African', 'Asian Fusion', 'Pizza', 'Tex-Mex', 'French', 'Chicken Wings', 'Internet Cafes', 'Caterers', 'Shaved Ice', 'Meat Shops', 'Cuban', 'Gastropubs', 'Event Planning & Services', 'Peruvian', 'Food Delivery Services', 'Creperies', 'Soup', 'Do-It-Yourself Food', 'Mexican', 'Halal', 'Dive Bars', 'Butcher', 'Golf', 'Southern', 'Polish', 'Street Vendors', 'British', 'Karaoke', 'Breakfast & Brunch', 'Hotels & Travel', 'Cafes', 'Vegetarian', 'Comfort Food', 'Modern European', 'Cambodian', 'Grocery', 'Bagels', 'Vegan', 'Tea Rooms', 'Szechuan', 'Bowling', 'Irish', 'Shopping', 'Dominican', 'Indian', 'Jazz & Blues', 'Barbeque', 'Fish & Chips', 'Gluten-Free', 'Diners', 'Kosher', 'Bars', 'Laotian', 'Soul Food', 'Italian', 'Active Life', 'Mongolian', 'Caribbean', 'Mediterranean', 'Home Services', 'Beer Bar', 'Hot Pot', 'Arts & Entertainment', 'Dim Sum', 'Cheese Shops', 'Latin American', 'Dance Clubs', 'Moroccan', 'Seafood', 'Convenience Stores', 'Korean', 'American (Traditional)', 'Coffee & Tea', 'Music Venues', 'Russian', 'Burgers']
	fields['General']['Attire'] = [row[0] for row in cur.execute('SELECT DISTINCT attire FROM yelp WHERE attire NOT NULL')].sort()

	for f in fields['General']:
		if(type(fields['General'][f]) == list):
			fields['General'][f].sort()
			fields['General'][f].insert(0, 'Not specified')

	conn.close()
	#logger.debug(str(fields))

	return render(request, "home/analysis.html", {"fields":fields})

def ratings(request):
	pass