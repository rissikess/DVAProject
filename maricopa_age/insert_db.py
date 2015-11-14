import sqlite3
import ast
import json

db = sqlite3.connect("E:/sanju/Master's/DVA/Project/maricopa_age/yelp_data.db")
cur = db.cursor()

cur.execute('DROP TABLE IF EXISTS yelp')
db.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS yelp 
				(
					"business_id" text primary key,
					"Payment Types_amex" integer,
					"Good for Kids" integer,
					"Open 24 Hours" integer,
					"Good For_brunch" integer,
					"Payment Types_visa" integer,
					"Music_live" integer,
					"Parking_garage" integer,
					"Female:20 to 29 years" integer,
					"Female:30 to 39 years" integer,
					"Thursday_close" text,
					"Accepts Credit Cards" integer,
					"Good For_latenight" integer,
					"Female:70 to 79 years" integer,
					"Parking_valet" integer,
					"Dogs Allowed" integer,
					"Music_dj" integer,
					"Ambience_classy" integer,
					"Good For_lunch" integer,
					"Payment Types_discover" integer,
					"Tuesday_open" text,
					"Dietary Restrictions_halal" integer,
					"$200000 or more" integer,
					"Monday_open" text,
					"Female:40 to 49 years" integer,
					"Order at Counter" integer,
					"Male:20 to 29 years" integer,
					"Coat Check" integer,
					"Corkage" integer,
					"Music_jukebox" integer,
					"Male:70 to 79 years" integer,
					"Price Range" integer,
					"Caters" integer,
					"Takes Reservations" integer,
					"Dietary Restrictions_vegan" integer,
					"$75000 to $99999" integer,
					"Ambience_divey" integer,
					"Ambience_romantic" integer,
					"Dietary Restrictions_gluten-free" integer,
					"Wi-Fi" integer,
					"Good For_dessert" integer, 
					"Happy Hour" integer,
					"Ambience_intimate" integer,
					"state" text,
					"Saturday_close" text,
					"review_count" integer,
					"Alcohol" integer,
					"Tuesday_close" text,
					"block_id" text,
					"Music_video" integer,
					"Dietary Restrictions_vegetarian" integer,
					"Female:0 to 9 years" integer,
					"$100000 to $124999" integer,
					"Ambience_touristy" integer,
					"longitude" real,
					"$25000 to $49999" integer,
					"type" text,
					"Friday_open" text,
					"Music_background_music" integer,
					"Take-out" integer,
					"Female:10 to 19 years" integer,
					"Parking_street" integer,
					"Female:60 to 69 years" integer,
					"Waiter Service" integer,
					"Payment Types_cash_only" integer,
					"Ambience_trendy" integer,
					"Male:50 to 59 years" integer,
					"Female:80 to and above" integer,
					"Dietary Restrictions_kosher" integer,
					"Good For Dancing" integer,
					"stars" integer,
					"$50000 to $74999" integer,
					"Wednesday_close" text,
					"neighborhoods" text,
					"Has TV" integer,
					"$10000 to $24999" integer,
					"Dietary Restrictions_soy-free" integer,
					"BYOB" integer,
					"Ages Allowed" text,
					"Male:10 to 19 years" integer,
					"Delivery" integer,
					"open" integer,
					"Friday_close" text,
					"Sunday_close" text,
					"By Appointment Only" integer,
					"Thursday_open" text, 
					"$150000 to $199999" integer,
					"Smoking" integer,
					"Wheelchair Accessible" integer,
					"Dietary Restrictions_dairy-free" integer,
					"Male:60 to 69 years" integer,
					"Ambience_hipster" integer,
					"Monday_close" text,
					"Drive-Thru" integer,
					"Female:50 to 59 years" integer,
					"Good For Groups" integer,
					"latitude" real,
					"Saturday_open" text,
					"$125000 to $149999" integer,
					"Payment Types_mastercard" integer,
					"Less than $10000" integer,
					"Male:40 to 49 years" integer,
					"Male:0 to 9 years" integer,
					"full_address" text,
					"Good For_breakfast" integer,
					"Male:80 to and above" integer,
					"Music_karaoke" integer,
					"city" text,
					"Ambience_casual" integer,
					"categories" text,
					"Wednesday_open" text,
					"Attire" text,
					"Ambience_upscale" integer,
					"Good For_dinner" integer,
					"name" text,
					"Parking_lot" integer,
					"BYOB/Corkage" integer,
					"Parking_validated" integer,
					"Good For Kids1" integer,
					"Outdoor Seating" integer,
					"Sunday_open" text,
					"Male:30 to 39 years" integer,
					"Noise Level" text
				)'''
			)

db.commit()

readfile = open('db_age.txt', 'r').readlines()

for line in readfile:
	print(readfile.index(line))
	line1 = line
	line = ast.literal_eval(line)
	columns = '", "'.join([i.strip() for i in line.keys()])
	columns = "\"" + columns + '\"' 
	placeholders = ', '.join('?' * len(line))
	sql = 'INSERT INTO yelp ({}) VALUES ({})'.format(columns, placeholders)
	#print (sql)
	cur.execute(sql, list(line.values()))
	db.commit()

db.commit()
db.close()
