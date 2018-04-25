import glob
import re
from pathlib import Path
import pandas as pd
from Scripts.Utils import *

def createScreenshot(files):
	global current_file
	file_iter = iter(files)
	
	def snapLayer():
		global current_file
		if not current_file:
			return;
		
		p = Path(current_file)
		layerName = p.stem
		iface.mapCanvas().saveAsImage("%s/Imgs/LayersMap/%s.png" % (base_dir, layerName))
		
		project = QgsProject.instance()
		layers = project.mapLayersByName(layerName)
		if len(layers) > 0:
			layer = layers[0]
			project.removeMapLayer(layer)
		setNextFeatureExtent()


	def setNextFeatureExtent():
		global current_file
		item = next(file_iter, None)
		if item is None:
			iface.mapCanvas().mapCanvasRefreshed.disconnect(snapLayer)
			print('Finished')
		else:			
			current_file = '%s/OCR/GeoJson/%s.json' % (base_dir,  item[0])
			rooftops_nearby = item[1]
		
			p = Path(current_file)
			layerName = p.stem
			
			vLayer = QgsVectorLayer(str(p), layerName, "ogr")
			if vLayer.featureCount() != 0:
				QgsProject.instance().addMapLayer(vLayer)
				try:
					symbols = vLayer.renderer().symbol()
					symbols.setColor(QColor.fromRgb(64 + int(191 * rooftops_nearby / 8.0), 0, 0, 0))
				except:
					print(layerName)
				
				vLayer.selectAll()
				iface.mapCanvas().zoomToSelected()
				iface.mapCanvas().zoomByFactor(1.5)
				vLayer.removeSelection()
				iface.mapCanvas().refreshAllLayers()
			else:
				setNextFeatureExtent()

	iface.mapCanvas().mapCanvasRefreshed.connect(snapLayer)
	setNextFeatureExtent()


# files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
Renewals_dataset = pd.read_csv('%sRenewals.csv' % data_dir)
rooftops = Renewals_dataset['rooftopsNearby'].as_matrix()
names = Renewals_dataset['district'].as_matrix()
createScreenshot(zip(names, rooftops))