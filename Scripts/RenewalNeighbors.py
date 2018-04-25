import pickle
import pandas as pd
import glob
from Scripts.Utils import *

csv_dir = data_dir + 'output.csv'
dataset = pd.read_csv(csv_dir)
coords = [QgsPointXY(*x) for x in dataset[['Lng','Lat']].values]

files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
df = pd.DataFrame(columns=('district', 'rooftopsNearby', 'closestRooftop', 'featuresCount', 'area'))
threshold = 300
#Create a measure object
distance = QgsDistanceArea()
# crs = QgsCoordinateReferenceSystem()
# crs.createFromSrsId(3857)
# distance.setSourceCrs(crs)
#distance.setEllipsoidalMode(True)
distance.setEllipsoid('WGS84')
for idx, f in enumerate(files):
	p = Path(f)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		# getting area data
		area = 0
		for f in vLayer.getFeatures():
			area += distance.measureArea(f.geometry())
		
		# getting rooftop data
		centroid = getLayerCenter(vLayer)
		centroid = QgsPointXY(*centroid)
		count = 0
		layerDistances = []
		for c in coords:
			m = distance.measureLine(centroid, c)
			layerDistances.append(m)
			if m < threshold:
				count += 1
		df.loc[idx] = [layerName, count, min(layerDistances), vLayer.featureCount(), area]

df.to_csv('%sRenewals.csv' % data_dir, index=False, encoding='utf-8')
