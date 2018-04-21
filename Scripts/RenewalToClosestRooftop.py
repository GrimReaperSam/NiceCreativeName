import pickle

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

base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/Project/'

csv_dir = base_dir + 'Data/output.csv'

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

with open('%s/Data/distances.pkl' % base_dir, 'wb') as fp:
    pickle.dump(distances, fp)