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
    print("hello")
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
    del fields['General']['Review_Count']


    fields['General']['City'] = ['Phoenix']
    fields['General']['Categories'] = ['Persian/Iranian', 'Cheesesteaks', 'Fondue', 'Food Court', 'Drugstores', 'Sandwiches', 'Chinese', 'Food Trucks', 'Ice Cream & Frozen Yogurt', 'Nightlife', 'Lounges', 'Shopping Centers', 'Hot Dogs', 'Real Estate', 'Buffets', 'Hotels', 'Vietnamese', 'Personal Chefs', 'Venues & Event Spaces', 'Hawaiian', 'Bubble Tea', 'Bakeries', 'Juice Bars & Smoothies', 'Wine Bars', 'Pubs', 'Thai', 'Tapas Bars', 'Shared Office Spaces', 'Pakistani', 'Spanish', 'Breweries', 'Food', 'Ethiopian', 'Steakhouses', 'Fruits & Veggies', 'Afghan', 'American (New)', 'Outlet Stores', 'Japanese', 'Middle Eastern', 'Ethnic Food', 'Health Markets', 'Indonesian', 'Sports Bars', 'Restaurants', 'Belgian', 'Sushi Bars', 'Gay Bars', 'Filipino', 'Beer, Wine & Spirits', 'Cocktail Bars', 'Live/Raw Food', 'Chocolatiers & Shops', 'Tapas/Small Plates', 'Cantonese', 'Food Stands', 'German', 'Delis', 'Arcades', 'Specialty Food', 'Greek', 'Salad', 'Brazilian', 'Fast Food', 'Cajun/Creole', 'Performing Arts', 'Donuts', 'Salvadoran', 'Desserts', 'Party & Event Planning', 'Herbs & Spices', 'African', 'Asian Fusion', 'Pizza', 'Tex-Mex', 'French', 'Chicken Wings', 'ernet Cafes', 'Caterers', 'Shaved Ice', 'Meat Shops', 'Cuban', 'Gastropubs', 'Event Planning & Services', 'Peruvian', 'Food Delivery Services', 'Creperies', 'Soup', 'Do-It-Yourself Food', 'Mexican', 'Halal', 'Dive Bars', 'Butcher', 'Golf', 'Southern', 'Polish', 'Street Vendors', 'British', 'Karaoke', 'Breakfast & Brunch', 'Hotels & Travel', 'Cafes', 'Vegetarian', 'Comfort Food', 'Modern European', 'Cambodian', 'Grocery', 'Bagels', 'Vegan', 'Tea Rooms', 'Szechuan', 'Bowling', 'Irish', 'Shopping', 'Dominican', 'Indian', 'Jazz & Blues', 'Barbeque', 'Fish & Chips', 'Gluten-Free', 'Diners', 'Kosher', 'Bars', 'Laotian', 'Soul Food', 'Italian', 'Active Life', 'Mongolian', 'Caribbean', 'Mediterranean', 'Home Services', 'Beer Bar', 'Hot Pot', 'Arts & Entertainment', 'Dim Sum', 'Cheese Shops', 'Latin American', 'Dance Clubs', 'Moroccan', 'Seafood', 'Convenience Stores', 'Korean', 'American (Traditional)', 'Coffee & Tea', 'Music Venues', 'Russian', 'Burgers']
    
    for f in fields['General']:
        if(type(fields['General'][f]) == list):
            fields['General'][f].sort()

    conn.close()
    #logger.debug(str(fields))
    #return None
    return render(request, "test/analysis.html", {"fields":fields})

@csrf_exempt
def getRestStats(request):
    con=None
    db_list=[]
    string = request.POST["value"]
    #string=string.lower()
    #print "Str",string
    d=json.loads(string)
    #print "Type of json",type(d)

    con = sqlite3.connect('yelp_data.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='yelp';")
    db_list=cursor.fetchall()

    db_tup=db_list[0]
    #print "Yelp table is",db_tup[0]
    count=[]
    query = "Select count(*), stars from "
    table = ""
    where = " where "
    for ele in d:
        if(ele=="general"):
            table += "yelp join "
            for i in d[ele]:

               col=i.lower()
               #print "Col is",type(col.decode("utf-8"))

               val=d[ele][i]
               #query =query+"where"
               #print type(val[0])
               if(val):
                   where += "("
                   for j in val:
                       if(val.index(j)==len(val)-1):
                           if(col == "categories"):
                                where=where +  col + " LIKE " +"'%" + j + "%'" ") and"
                           else:
                                where=where+(col+"= '"+j+"'")+") and "
                       else:
                           if(col == "categories"):
                                where=where + col + " LIKE " +"'%" + j + "%'" " or"
                           else:
                                where=where+(col+"= '"+j+"'")+" or "

               #query=query+" and "
                       #print col,j
                   #print col ,type(val)

                #count = cursor.execute("SELECT count(*) FROM yelp WHERE ='Phoenix' and Price_Range='1' or Price_Range='2' and State='Phoenix'")
                #print count
        elif(ele=="hours"):
            pass
        else:
            if(len(d[ele])!=0):
                table += ele + " join "
                if(len(d[ele]) > 1):
                    where += "("
                    for i in d[ele]:
                        where += ele + "." + i + "=1 or "
                    where = where[:-3] + ") and "
                else:
                    where += "("
                    for i in d[ele]:
                        where += ele + "." + i + "=1 "
                    where += ") and "
                where += ele + ".b_id=" + "yelp.business_id and "

    query = query + table[:-5] + where[:-4] + " group by stars"
    print (query)
    cn=cursor.execute(query)
    cn= cn.fetchall()
    #cn=cn[0]
    pie_dict={}
    pie_list=[]
    j=0.5
    for i in cn:
        j=j+0.5
        pie_dict["label"]=str(j)
        pie_dict["value"]=i[0]
        pie_list.append(pie_dict.copy())
    #print pie_list
        #print j,",",i[0]

    pie_json=json.dumps(pie_list)
    return HttpResponse(pie_json)