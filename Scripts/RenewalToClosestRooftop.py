import pickle
import pandas as pd
from Scripts.Utils import *


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