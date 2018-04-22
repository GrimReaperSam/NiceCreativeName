import pickle
import pandas as pd
from Scripts.Utils import *

def getLayerCenter(layer):
	features = layer.getFeatures()
	a = None
	for f in features:
		errors = f.geometry().validateGeometry()
		if len(errors) == 0:
			if a is None:
				a = f.geometry()
			else:
				a = a.combine(f.geometry())
	
	return a.centroid().asPoint()

csv_dir = data_dir + 'output.csv'

dataset = pd.read_csv(csv_dir)
coords = [QgsPointXY(*x) for x in dataset[['Lng','Lat']].values]

files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
distances = []
for f in files:
	p = Path(f)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		centroid = getLayerCenter(vLayer)
		centroid = QgsPointXY(*centroid)
		layerDistances = []
		for c in coords:
			layerDistances.append(centroid.sqrDist(c))
		distances.append((layerName, min(layerDistances)))

with open('%s/distances.pkl' % data_dir, 'wb') as fp:
    pickle.dump(distances, fp)