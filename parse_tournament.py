import mysql.connector
import json
from urllib2 import urlopen
from dateutil import parser as timeparser

def prompt(type, value):
	return raw_input("Retrieved "+type+": "+value+". Press Enter if this is correct or type the correct value:\n\t") or value

db_connection = mysql.connector.connect(
		user='root',
		password='paradise',#'chunkylove69@aol.com',
		host='localhost',
		database='MeleeData'
	)
db_cursor = db_connection.cursor()

while True:
	entry = {}
	host = raw_input("Enter a bracket host, eg. smash.gg or challonge.com (q to exit):\n\t")
	if host == 'q':
		break

	if host == 'c' or host == 'challonge' or host == 'challonge.com':
		entry['host'] = 'challonge'

		entry['id_string'] = raw_input("Enter an id string, eg. michigansmash-umeme54:\n\t")
		if entry['id_string'] == 'q':
			continue

		data = {}
		try:
			for data_type, subpath in [(t, entry['id_string']+s) for t,s in [('tournament',''),('matches','/matches')]]:
				uri = 'https://api.challonge.com/v1/tournaments/'+subpath+'.json'
				print("Contacting API at %s..." % uri)
				data[data_type] = json.loads(urlopen(uri+'?api_key=XBFwcbaWSvrfHiaNONNgwyfPo8LrYozALwIWfkBd').read())
		except Exception as e:
			print(e)
			print("Error accessing %s." % uri)
			continue
		data['tournament'] = data['tournament']['tournament']
		entry['name'] = prompt('name', data['tournament']['name'])
		entry['date'] = prompt('date', timeparser.parse(data['tournament']['started_at']).date())

		series_parts = entry['name'].rsplit(None, 1)
		if len(series_parts) == 2 and all(c in '0123456789XVI' for c in series_parts[1]):
			series = series_parts[0]
		else:
			series = ''
		entry['series'] = prompt('series', series)

		entry['entrants'] = data['tournament']['participants_count']

		for match in data['matches']:
			match = match['match']

		# id        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
		# id_string VARCHAR(100) NOT NULL,
		# host      VARCHAR(16)  NOT NULL,
		# name      VARCHAR(100) NOT NULL,
		# series    VARCHAR(100),
		# location  VARCHAR(100) NOT NULL,
		# date      TIMESTAMP    NOT NULL

	if host == 's' or host == 'smash.gg':
		pass
