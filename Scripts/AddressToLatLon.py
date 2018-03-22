import sys
import geocoder
import pandas as pd

key = 'efOlHAySH1y4iscNjRp5muxVlEbLpt21'

def getLatLon(name):
	print(name)
	g = geocoder.mapquest(name, key=key)
	if g.status == 'OK':
		return (g.lat, g.lng)
	return (None, None)

if __name__ == "__main__":
	csv_name = sys.argv[1]
	
	csv_input = pd.read_csv(csv_name)
	csv_input['Address'] = csv_input['sec']+csv_input['addr']
	csv_input['Lat'], csv_input['Lng'] = zip(*csv_input['Address'].map(getLatLon))
	csv_input.to_csv('output.csv', index=False, encoding='utf-8')