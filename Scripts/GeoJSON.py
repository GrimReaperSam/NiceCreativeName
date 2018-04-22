import glob
import re
from pathlib import Path

base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/NiceCreativeName/'


def createScreenshot(files):
	global current_file
	file_iter = iter(files)
	
	def snapLayer():
		global current_file
		if not current_file:
			return;
		
		p = Path(current_file)
		layerName = p.stem
		iface.mapCanvas().saveAsImage("%s/Imgs/LayersBG/%s.png" % (base_dir, layerName))
		
		project = QgsProject.instance()
		layers = project.mapLayersByName(layerName)
		if len(layers) > 0:
			layer = layers[0]
			project.removeMapLayer(layer)
		setNextFeatureExtent()


	def setNextFeatureExtent():
		global current_file
		current_file = next(file_iter, None)
		if current_file is None:
			iface.mapCanvas().mapCanvasRefreshed.disconnect(snapLayer)
			print('Finished')
		else:
			p = Path(current_file)
			layerName = p.stem
			
			vLayer = QgsVectorLayer(str(p), layerName, "ogr")
			if vLayer.featureCount() != 0:
				QgsProject.instance().addMapLayer(vLayer)
				try:
					symbols = vLayer.renderer().symbol()
					symbols.setColor(QColor.fromRgb(255, 255, 255, 0))
				except:
					print(layerName)
				
				vLayer.selectAll()
				iface.mapCanvas().zoomToSelected()
				vLayer.removeSelection()
				iface.mapCanvas().refreshAllLayers()
			else:
				setNextFeatureExtent()

	iface.mapCanvas().mapCanvasRefreshed.connect(snapLayer)
	setNextFeatureExtent()


files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
createScreenshot(files)