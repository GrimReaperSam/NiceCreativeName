import sys
import geocoder
import pandas as pd

# Transform illegal rooftop data into useful Lat/Lon coordinates

mapquest_key = 'efOlHAySH1y4iscNjRp5muxVlEbLpt21'
googlemaps_key = 'AIzaSyC-NIgKjVSQKxzx9quLrhJhCrGZ1AViKW8'

def getLatLon(name):
	print(name)
	g = geocoder.google(name, key=googlemaps_key)
	if g.status == 'OK':
		return (g.lat, g.lng)
	return (None, None)

if __name__ == "__main__":
	csv_name = sys.argv[1]
	
	csv_input = pd.read_csv(csv_name)
	csv_input['Address'] = csv_input['sec']+csv_input['addr']
	csv_input['Lat'], csv_input['Lng'] = zip(*csv_input['Address'].map(getLatLon))
	csv_input.to_csv('../Data/Output-g.csv', index=False, encoding='utf-8')