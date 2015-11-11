import sqlite3
import ast

db = sqlite3.connect("E:/sanju/Master's/DVA/Project/maricopa_age/yelp_data.db")
cur = db.cursor()

cur.execute('DROP TABLE IF EXISTS yelp')


cur.execute('''CREATE TABLE IF NOT EXISTS yelp 
				(
					"business_id" text primary key,
					"Payment Types_amex" text,
					"Good for Kids" text,
					"Open 24 Hours" text,
					"Good For_brunch" text,
					"Payment Types_visa" text,
					"Music_live" text,
					"Parking_garage" text,
					"Female:20 to 29 years" text,
					"Female:30 to 39 years" text,
					"Thursday_close" text,
					"Accepts Credit Cards" text,
					"Good For_latenight" text,
					"Female:70 to 79 years" text,
					"Parking_valet" text,
					"Dogs Allowed" text,
					"Music_dj" text,
					"Ambience_classy" text,
					"Good For_lunch" text,
					"Payment Types_discover" text,
					"Tuesday_open" text,
					"Dietary Restrictions_halal" text,
					"$200000 or more" text,
					"Monday_open" text,
					"Female:40 to 49 years" text,
					"Order at Counter" text,
					"Male:20 to 29 years" text,
					"Coat Check" text,
					"Corkage" text,
					"Music_jukebox" text,
					"Male:70 to 79 years" text,
					"Price Range" text,
					"Caters" text,
					"Takes Reservations" text,
					"Dietary Restrictions_vegan" text,
					"$75000 to $99999" text,
					"Ambience_divey" text,
					"Ambience_romantic" text,
					"Dietary Restrictions_gluten-free" text,
					"Wi-Fi" text,
					"Good For_dessert" text, 
					"Happy Hour" text,
					"Ambience_intimate" text,
					"state" text,
					"Saturday_close" text,
					"review_count" text,
					"Alcohol" text,
					"Tuesday_close" text,
					"block_id" text,
					"Music_video" text,
					"Dietary Restrictions_vegetarian" text,
					"Female:0 to 9 years" text,
					"$100000 to $124999" text,
					"Ambience_touristy" text,
					"longitude" real,
					"$25000 to $49999" text,
					"type" text,
					"Friday_open" text,
					"Music_background_music" text,
					"Take-out" text,
					"Female:10 to 19 years" text,
					"Parking_street" text,
					"Female:60 to 69 years" text,
					"Waiter Service" text,
					"Payment Types_cash_only" text,
					"Ambience_trendy" text,
					"Male:50 to 59 years" text,
					"Female:80 to and above" text,
					"Dietary Restrictions_kosher" text,
					"Good For Dancing" text,
					"stars" text,
					"$50000 to $74999" text,
					"Wednesday_close" text,
					"neighborhoods" text,
					"Has TV" text,
					"$10000 to $24999" text,
					"Dietary Restrictions_soy-free" text,
					"BYOB" text,
					"Ages Allowed" text,
					"Male:10 to 19 years" text,
					"Delivery" text,
					"open" text,
					"Friday_close" text,
					"Sunday_close" text,
					"By Appointment Only" text,
					"Thursday_open" text, 
					"$150000 to $199999" text,
					"Smoking" text,
					"Wheelchair Accessible" text,
					"Dietary Restrictions_dairy-free" text,
					"Male:60 to 69 years" text,
					"Ambience_hipster" text,
					"Monday_close" text,
					"Drive-Thru" text,
					"Female:50 to 59 years" text,
					"Good For Groups" text,
					"latitude" real,
					"Saturday_open" text,
					"$125000 to $149999" text,
					"Payment Types_mastercard" text,
					"Less than $10000" text,
					"Male:40 to 49 years" text,
					"Male:0 to 9 years" text,
					"full_address" text,
					"Good For_breakfast" text,
					"Male:80 to and above" text,
					"Music_karaoke" text,
					"city" text,
					"Ambience_casual" text,
					"categories" text,
					"Wednesday_open" text,
					"Attire" text,
					"Ambience_upscale" text,
					"Good For_dinner" text,
					"name" text,
					"Parking_lot" text,
					"BYOB/Corkage" text,
					"Parking_validated" text,
					"Good For Kids1" text,
					"Outdoor Seating" text,
					"Sunday_open" text,
					"Male:30 to 39 years" text,
					"Noise Level" text
				)'''
			)

db.commit()

readfile = open('db_age.txt', 'r').readlines()

for line in readfile:
	line1 = line
	line = ast.literal_eval(line)
	columns = '", "'.join([i.strip() for i in line.keys()])
	columns = "\"" + columns + '\"' 
	placeholders = ', '.join('?' * len(line))
	sql = 'INSERT INTO yelp ({}) VALUES ({})'.format(columns, placeholders)
	#print (sql)
	print(readfile.index(line1))
	cur.execute(sql, ["'" + str(i) + "'" for i in line.values()])
	db.commit()

db.commit()
db.close()
