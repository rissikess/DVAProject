from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.conf import settings as djangoSettings

import json
import logging
import sqlite3

logger = logging.getLogger(__name__)
@csrf_exempt
def home(request):
	conn = sqlite3.connect('yelp_data.db')
	cur = conn.cursor()
	tables_list = ['payment_types', 'ambience', 'meal_type', 'perks', 'dietary_restrictions', 'music', 'parking', "hours", "yelp"]
	fields = {}
	hours = ["000"]
	hours.extend(list(range(100, 1000, 100)))
	hours = ["0" + str(i) for i in hours]
	hours.extend(list(range(1000, 2500, 100)))
	for table in tables_list:
		cursor = cur.execute('select * from ' + table + ' limit 1')
		if(table == "yelp"):
			fields['General'] = {description[0].replace(" ", " ").title():0 for description in cursor.description[1:]}
		elif(table == "hours"):
			fields['Hours'] = {}
		else:
			fields[table.replace(" ", " ").title()] = [description[0].replace(" ", " ").title() for description in cursor.description[1:]]

	# hour fields
	for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
		fields['Hours'][day + " open"] = hours
		fields['Hours'][day + " closed"] = hours

	#logger.debug(fields['Hours'])
	# general fields
	fields['General']['Price Range'] = [row[0] for row in cur.execute('SELECT DISTINCT price_range FROM yelp where price_range NOT NULL')]
	fields['General']['State'] = ['AZ']
	del fields['General']['Block_Id']
	del fields['General']['Latitude']
	del fields['General']['Longitude']
	del fields['General']['Type']
	del fields['General']['Neighborhoods']
	del fields['General']['Ages_Allowed']
	del fields['General']['Open']
	del fields['General']['Full_Address']
	del fields['General']['Name']
	del fields['General']['Stars']
	del fields['General']['Attire']

	fields['General']['City'] = ['Phoenix']
	fields['General']['Categories'] = ['Persian/Iranian', 'Cheesesteaks', 'Fondue', 'Food Court', 'Drugstores', 'Sandwiches', 'Chinese', 'Food Trucks', 'Ice Cream & Frozen Yogurt', 'Nightlife', 'Lounges', 'Shopping Centers', 'Hot Dogs', 'Real Estate', 'Buffets', 'Hotels', 'Vietnamese', 'Personal Chefs', 'Venues & Event Spaces', 'Hawaiian', 'Bubble Tea', 'Bakeries', 'Juice Bars & Smoothies', 'Wine Bars', 'Pubs', 'Thai', 'Tapas Bars', 'Shared Office Spaces', 'Pakistani', 'Spanish', 'Breweries', 'Food', 'Ethiopian', 'Steakhouses', 'Fruits & Veggies', 'Afghan', 'American (New)', 'Outlet Stores', 'Japanese', 'Middle Eastern', 'Ethnic Food', 'Health Markets', 'Indonesian', 'Sports Bars', 'Restaurants', 'Belgian', 'Sushi Bars', 'Gay Bars', 'Filipino', 'Beer, Wine & Spirits', 'Cocktail Bars', 'Live/Raw Food', 'Chocolatiers & Shops', 'Tapas/Small Plates', 'Cantonese', 'Food Stands', 'German', 'Delis', 'Arcades', 'Specialty Food', 'Greek', 'Salad', 'Brazilian', 'Fast Food', 'Cajun/Creole', 'Performing Arts', 'Donuts', 'Salvadoran', 'Desserts', 'Party & Event Planning', 'Herbs & Spices', 'African', 'Asian Fusion', 'Pizza', 'Tex-Mex', 'French', 'Chicken Wings', 'ernet Cafes', 'Caterers', 'Shaved Ice', 'Meat Shops', 'Cuban', 'Gastropubs', 'Event Planning & Services', 'Peruvian', 'Food Delivery Services', 'Creperies', 'Soup', 'Do-It-Yourself Food', 'Mexican', 'Halal', 'Dive Bars', 'Butcher', 'Golf', 'Southern', 'Polish', 'Street Vendors', 'British', 'Karaoke', 'Breakfast & Brunch', 'Hotels & Travel', 'Cafes', 'Vegetarian', 'Comfort Food', 'Modern European', 'Cambodian', 'Grocery', 'Bagels', 'Vegan', 'Tea Rooms', 'Szechuan', 'Bowling', 'Irish', 'Shopping', 'Dominican', 'Indian', 'Jazz & Blues', 'Barbeque', 'Fish & Chips', 'Gluten-Free', 'Diners', 'Kosher', 'Bars', 'Laotian', 'Soul Food', 'Italian', 'Active Life', 'Mongolian', 'Caribbean', 'Mediterranean', 'Home Services', 'Beer Bar', 'Hot Pot', 'Arts & Entertainment', 'Dim Sum', 'Cheese Shops', 'Latin American', 'Dance Clubs', 'Moroccan', 'Seafood', 'Convenience Stores', 'Korean', 'American (Traditional)', 'Coffee & Tea', 'Music Venues', 'Russian', 'Burgers']
	fields['General']['Review_Count'] = [str(i) + " - " + str(i + 50) for i in range(0, 300, 50)]
	fields['General']['Review_Count'].append('350 and above')
	for f in fields['General']:
		if(type(fields['General'][f]) == list):
			fields['General'][f].sort()

	conn.close()
	#logger.debug(str(fields))

	return render(request, "analysis.html", {"fields":fields})

@csrf_exempt
def getStats(request):
	json_obj = json.loads(request.POST["value"])
	
	count = 0
	for i in json_obj:
		if(json_obj[i] != "null" or len(json_obj[i]) != 0):
			count += 1

	print("Count: " + str(count))
	data = open(djangoSettings.STATIC_ROOT + "/phoenixrestaurantsageincome.json", 'r').readlines()
	#data = json.loads(datafile)
	age_fields = ['female:0 to 9 years','female:10 to 19 years', 'female:20 to 29 years', 'female:30 to 39 years', 'female:40 to 49 years', 'female:50 to 59 years', "female:60 to 69 years" , "female:70 to 79 years" , "female:80 and above", "male:0 to 9 years", "male:10 to 19 years", "male:20 to 29 years", "male:30 to 39 years", "male:40 to 49 years", "male:50 to 59 years", "male:60 to 69 years", "male:70 to 79 years", "male:80 and above"]
	income_fields = ["less than $10000" ,  "$200000 or more",  "$75000 to $99999" ,  "$100000 to $124999" ,  "$25000 to $49999" ,  "$50000 to $74999" ,  "$10000 to $24999" , "$150000 to $199999",  "$125000 to $149999"]
	age_dict = {1:{x:[] for x in age_fields}, 1.5:{x:[] for x in age_fields}, 2:{x:[] for x in age_fields}, 2.5:{x:[] for x in age_fields}, 3:{x:[] for x in age_fields}, 3.5:{x:[] for x in age_fields}, 4:{x:[] for x in age_fields}, 4.5:{x:[] for x in age_fields}, 5:{x:[] for x in age_fields}}
	income_dict = {1:{x:[] for x in income_fields}, 1.5:{x:[] for x in income_fields}, 2:{x:[] for x in income_fields}, 2.5:{x:[] for x in income_fields}, 3:{x:[] for x in income_fields}, 3.5:{x:[] for x in income_fields}, 4:{x:[] for x in income_fields}, 4.5:{x:[] for x in income_fields}, 5:{x:[] for x in income_fields}}
	for entry in data:
		entry = json.loads(entry.lower())
		flag = True
		encount = 0
		for i in json_obj:
			if(i.lower() == "general"):
				for j in json_obj[i]:
					if(json_obj[i][j] != "null"):
						if(j.lower() == "categories"):
							if(len(set(entry[j.lower()]).intersection(set(json_obj[i][j]))) == 0):
								flag = False
								
						else:
							if(str(entry[j.lower()]) not in [z.lower() for z in json_obj[i][j]]):
								print(str(entry[j.lower()]))
								print(json_obj[i][j])
								flag = False
								
					if(flag == False):
						break

				if(flag == True):
					encount += 1
				else:
					break

			else:
				if(i.lower() == "perks"):
					for p in json_obj[i]:
						if(p != None):
							if(p not in entry["attributes"] or entry["attributes"][p] != True):
								flag = False
				else:
					for el in json_obj[i]:
						if(entry["attributes"][i.title()][el] != True):
							print("entered")
							print(el)
							print(i)
							flag = False

				if(flag == True):
					encount += 1
				else:
					break

			if(flag == True):
				encount += 1
		#print("ENCOUNT: " + str(encount))
		if(encount >= count):
			for a in age_fields:
				if(a in entry):
					#print("entered")
					age_dict[entry["stars"]][a].append(entry[a])
			for inc in income_fields:
				if(inc in entry):
					income_dict[entry["stars"]][inc].append(entry[inc])

	for rating in age_dict:
		for age in age_dict[rating]:
			if(len(age_dict[rating][age]) > 0):
				age_dict[rating][age] = float(sum(age_dict[rating][age]))/len(age_dict[rating][age])
			else:
				age_dict[rating][age] = 0

	for rating in income_dict:
		for income in income_dict[rating]:
			if(len(income_dict[rating][income]) > 0):
				income_dict[rating][income] = float(sum(income_dict[rating][income]))/len(income_dict[rating][income])
			else:
				income_dict[rating][income] = 0

	return HttpResponse(json.dumps({"age":age_dict, "income":income_dict}))