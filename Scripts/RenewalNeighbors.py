import pickle
import pandas as pd
from Scripts.Utils import *

csv_dir = data_dir + 'output.csv'
dataset = pd.read_csv(csv_dir)
coords = [QgsPointXY(*x) for x in dataset[['Lng','Lat']].values]

files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
neighbors = []
threshold = 1.2173805738107589e-05
for f in files:
	p = Path(f)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		centroid = getLayerCenter(vLayer)
		centroid = QgsPointXY(*centroid)
		count = 0
		for c in coords:
			if centroid.sqrDist(c) < threshold:
				count += 1
		neighbors.append((layerName, count))

with open('%s/neighbors.pkl' % data_dir, 'wb') as fp:
    pickle.dump(neighbors, fp)