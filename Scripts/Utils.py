base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/NiceCreativeName/'
data_dir = base_dir + 'Data/'

def remove_markers():
	canvas = iface.mapCanvas()
	scene = canvas.scene()
	vertex_items = [i for i in scene.items() if issubclass(type(i), qgis.gui.QgsVertexMarker)]
	for ver in vertex_items:
		if ver in scene.items():
			scene.removeItem(ver)
	canvas.refresh()

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