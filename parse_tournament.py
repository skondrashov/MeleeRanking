import mysql.connector
import json
import requests

def prompt(type, value):
	return input("Retrieved "+type+": "+value+". Press Enter if this is correct or type the correct value:\n\t") or value

db_connection = mysql.connector.connect(
		user='root',
		password='root',
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
			for data_type, subpath in [(t, entry['id_string']+s) for t,s in [('tournament',''),('matches','/matches'),('participants','/participants')]]:
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

		#print(json.dumps(entry,indent=4))
		#print(json.dumps(data,indent=4))
		# id        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
		# id_string VARCHAR(100) NOT NULL,
		# host      VARCHAR(16)  NOT NULL,
		# name      VARCHAR(100) NOT NULL,
		# series    VARCHAR(100),
		# location  VARCHAR(100) NOT NULL,
		# date      TIMESTAMP    NOT NULL

		#------enter into db--------
		#check if tourney already has been entered in table
		db_cursor.execute("SELECT * FROM tournaments WHERE id_string = %s LIMIT 1;", (entry['id_string'],))
		if db_cursor.fetchone() is not None:
			print("Tournament already in table")
			continue
		#tourney has not been entered, insert tourney info
		db_cursor.execute("INSERT INTO tournaments (id_string, host, name, series, location ,date) VALUES (%s, %s, %s, %s, 'MI', %s);",
			(entry['id_string'], entry['host'], entry['name'], entry['series'], entry['date']))
		db_connection.commit()
		print("Successfully inserted tournament")

		#insert players into table
		for participant in data['participants']:
			participant = participant['participant']
			name = participant['name']
			if '|' in name:
				tag = name.split('|')[1]
				sponsor = name.split('|')[0]
			else:
				tag = name
				sponsor = None
			player_in_db = None
			db_cursor.execute("SELECT sponsor FROM players WHERE tag = (%s) LIMIT 1;",(tag,))
			player_in_db = db_cursor.fetchone()
			#check for player in db
			if player_in_db is not None:
				#check if sponsor needs to be updated
				if player_in_db[0] != sponsor:
					db_cursor.execute("UPDATE players SET sponsor = '%s';", (sponsor))
					db_connection.commit()
					print("Player: " + tag + " sponsor updated to " + sponsor)
				continue
			

			#insert player into db
			if sponsor is None:
				db_cursor.execute("INSERT INTO players (tag) VALUES (%s);",(tag,))
			else:
				db_cursor.execute("INSERT INTO players (tag, sponsor) VALUES (%s, %s);", (tag, sponsor))
			db_connection.commit()
			print("Player " + tag + " inserted into db")






	if host == 's' or host == 'smash.gg':
		pass
