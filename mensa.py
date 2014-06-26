#! /usr/local/bin/python
import argparse
import requests
from lxml import html 
from lxml.cssselect import CSSSelector
import datetime
import calendar
day_mappings = {"mon":"mo", "tue":"di", "wed":"mi", "thu":"do", "fri":"fr", "sat":"sa"}
arg_parser = argparse.ArgumentParser(description="Display the menu of the Mensa 1 in Braunschweig")
arg_parser.add_argument('day', nargs='?', default='today', help='The day of the week for which the menu should be displayed. Format: Mon, Tue, Wed, Thu, Fri, Sat, Sun')
arg_parser.add_argument('timeslot', nargs='?', default='all', help='Determines which timeslot (mm = Mittagsmensa, am = Abendmensa) to display')
args = arg_parser.parse_args()
req = requests.get("http://www.stw-on.de/braunschweig/essen/menus/mensa-1")
content = req.text
mensaHtml = html.fromstring(content)
sel = CSSSelector("table.swbs_speiseplan") 

if args.day == 'today':
	args.day = calendar.day_abbr[datetime.datetime.today().weekday()].lower()

abendmensa = 0 #There are two tables for each day; the first one for the Mittagsmensa, and the second one for the Abendmensa. Thus we need to count.
for e in sel(mensaHtml):
	if (e.get('id') == 'swbs_speiseplan_' + day_mappings[args.day]): 
		headers = e.cssselect('th.swbs_speiseplan_head')
		plan = e.cssselect('td.swbs_speiseplan_meal')
		if (args.timeslot == 'all' or args.timeslot == 'mm') and abendmensa == 0:
			print headers[0].text_content() + "\n"
			for meal in plan:
				print "\t" +  meal.text_content()
		if args.timeslot == 'all':
			print ""
		if args.timeslot != 'mm' and (args.timeslot == 'all' or args.timeslot == 'am') and abendmensa == 1:
			print headers[0].text_content() + "\n" 
    			for meal in plan:
				print "\t" +  meal.text_content()
		abendmensa += 1 
#	day_menu = e.cssselect('table#swbs_speiseplan_' + args.day)
	
	for meal in e.cssselect('td.swbs_speiseplan_meal'):
		meal.text_content()
