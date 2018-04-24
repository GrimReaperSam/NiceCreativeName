import pickle
import pandas as pd
from Scripts.Utils import *

csv_dir = data_dir + 'output.csv'
dataset = pd.read_csv(csv_dir)
coords = [QgsPointXY(*x) for x in dataset[['Lng','Lat']].values]

files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
df = pd.DataFrame(columns=('district', 'rooftopsNearby', 'closestRooftop', 'featuresCount'))
threshold = 1.2173805738107589e-05
for idx, f in enumerate(files):
	p = Path(f)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		centroid = getLayerCenter(vLayer)
		centroid = QgsPointXY(*centroid)
		count = 0
		layerDistances = []
		for c in coords:
			layerDistances.append(centroid.sqrDist(c))
			if centroid.sqrDist(c) < threshold:
				count += 1
		df.loc[idx] = [layerName, count, min(layerDistances), vLayer.featureCount()]

df.to_csv('%sRenewals.csv' % data_dir, index=False, encoding='utf-8')
