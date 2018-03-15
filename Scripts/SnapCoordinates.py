import sys
base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/Project/Imgs/'


current_coord = None
def createScreenshot(coords):
	global current_coord
	coords_iter = iter(coords)
	
	def exportMap():
		global current_coord
		print(current_coord)
		if not current_coord:
			return;
		qgis.utils.iface.mapCanvas().saveAsImage("%s%.3f%.3f.png" % (base_dir, current_coord[0], current_coord[1]))
		setNextFeatureExtent()


	def setNextFeatureExtent():
		global current_coord
		current_coord = next(coords_iter, None)
		if current_coord is None:
			qgis.utils.iface.mapCanvas().mapCanvasRefreshed.disconnect( exportMap)
		else:
			a = QgsPointXY (*current_coord)
			qgis.utils.iface.mapCanvas().setCenter(a)
			qgis.utils.iface.mapCanvas().refreshAllLayers()


	qgis.utils.iface.mapCanvas().mapCanvasRefreshed.connect( exportMap)
	setNextFeatureExtent()

coords = [(121.535530, 25.052545), (121.529050,25.050271), (121.527214, 25.039836)]
createScreenshot(coords)