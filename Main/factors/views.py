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
	tables_list = ['age', 'income_range', 'payment_types', 'ambience', 'meal_type', 'perks', 'dietary_restrictions', 'music', 'yelp', 'hours', 'parking']
	fields = {}
	for table in tables_list:
		cursor = cur.execute('select * from ' + table + ' limit 1')
		if(table == "yelp"):
			table = "general"
		fields[table.replace("_", " ").title()] = [description[0].replace("_", " ").title() for description in cursor.description[1:]]
	conn.close()
	#logger.debug(str(fields))

	return render(request, "home/analysis.html", {"fields":fields})

def ratings(request):
	pass