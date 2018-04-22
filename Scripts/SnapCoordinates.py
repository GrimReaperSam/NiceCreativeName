import sys
import pandas as pd
from Scripts.Utils import *

csv_dir = data_dir + 'output.csv'
img_dir = base_dir + 'GImgs3/'

current_coord = None
def createScreenshot(coords):
	global current_coord
	coords_iter = iter(coords)
	
	def exportMap():
		global current_coord
		print(current_coord)
		if not current_coord:
			return;
		if current_coord[1] is not None:
			qgis.utils.iface.mapCanvas().saveAsImage("%s%s.png" % (img_dir, current_coord[0]))
		setNextFeatureExtent()


	def setNextFeatureExtent():
		global current_coord
		current_coord = next(coords_iter, None)
		if current_coord is None:
			qgis.utils.iface.mapCanvas().mapCanvasRefreshed.disconnect(exportMap)
		else:
			a = QgsPointXY (*current_coord[1:])
			qgis.utils.iface.mapCanvas().setCenter(a)
			qgis.utils.iface.mapCanvas().refreshAllLayers()


	qgis.utils.iface.mapCanvas().mapCanvasRefreshed.connect(exportMap)
	setNextFeatureExtent()


dataset = pd.read_csv(csv_dir)
coords = [tuple(x) for x in dataset[['Address', 'Lng','Lat']].values]
createScreenshot(coords)