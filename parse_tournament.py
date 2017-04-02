import mysql.connector
import json
import requests

def prompt(type, value):
	return input("Retrieved "+type+": "+value+". Press Enter if this is correct or type the correct value:\n\t") or value

db_connection = mysql.connector.connect(
		user='root',
		password='root',#'chunkylove69@aol.com',
		host='localhost',
		database='MeleeData'
	)
db_cursor = db_connection.cursor()

while True:
	entry = {}
	host = input("Enter a bracket host, eg. smash.gg or challonge.com (q to exit):\n\t")
	if host == 'q':
		break

	if host == 'c' or host == 'challonge' or host == 'challonge.com':
		entry['host'] = 'challonge'

		entry['id_string'] = input("Enter an id string, eg. michigansmash-umeme54:\n\t")
		if entry['id_string'] == 'q':
			continue

		data = {}
		try:
			for data_type, subpath in [(t, entry['id_string']+s) for t,s in [('tournament',''),('matches','/matches')]]:
				uri = 'https://api.challonge.com/v1/tournaments/'+subpath+'.json'
				print("Contacting API at %s..." % uri)
				response = requests.get(uri+'?api_key=XBFwcbaWSvrfHiaNONNgwyfPo8LrYozALwIWfkBd')
				data[data_type] = response.json()
		except Exception as e:
			print("Error accessing %s." % uri)
			print(e)
			continue
		data['tournament'] = data['tournament']['tournament']
		entry['name'] = prompt('name', data['tournament']['name'])
		entry['date'] = prompt('date', data['tournament']['started_at'])
		entry['date'] = entry['date'].split('T')[0] + " " + entry['date'].split('T')[1]
		entry['date'] = entry['date'][:-6] 

		series_parts = entry['name'].rsplit(None, 1)
		if len(series_parts) == 2 and all(c in '0123456789XVI' for c in series_parts[1]):
			series = series_parts[0]
		else:
			series = ''
		entry['series'] = prompt('series', series)

		entry['entrants'] = data['tournament']['participants_count']

		print(json.dumps(entry,indent=4))
		# id        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
		# id_string VARCHAR(100) NOT NULL,
		# host      VARCHAR(16)  NOT NULL,
		# name      VARCHAR(100) NOT NULL,
		# series    VARCHAR(100),
		# location  VARCHAR(100) NOT NULL,
		# date      TIMESTAMP    NOT NULL

		#enter into db
		insert_string = ("INSERT INTO tournaments (id_string, host ,name ,series ,location ,date) VALUES ('" + 
			entry['id_string'] + "', '" + entry['host'] + "', '" + entry['name'] + "', '" + entry['series'] + "', '" +
			"MI" + "', '" + entry['date'] + "');")
		db_cursor.execute(insert_string)
		db_connection.commit()
		print("Successfully inserted tournament")




	if host == 's' or host == 'smash.gg':
		pass


