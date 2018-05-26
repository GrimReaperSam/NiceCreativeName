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
		iface.mapCanvas().saveAsImage("%s/Imgs/LayersRGB 2013 HIGHER/%s.png" % (base_dir, layerName))
		
		project = QgsProject.instance()
		layers = project.mapLayersByName(layerName)
		polygonLayers = project.mapLayersByName('polygon')
		if len(layers) > 0:
			project.removeMapLayer(layers[0])
			project.removeMapLayer(polygonLayers[0])
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
					symbols.symbolLayer(0).setStrokeColor(QColor.fromRgb(0,0,0,0))
				except:
					print(layerName)
				
				vLayer.selectAll()
				iface.mapCanvas().zoomToSelected()
				iface.mapCanvas().zoomByFactor(1.5)
				
				# TEST CODE
				layer22 = QgsVectorLayer('Polygon?crs=epsg:4326', 'polygon', 'memory')
				prov = layer22.dataProvider()
				pointCenter = iface.mapCanvas().extent()
				pointCenter = vLayer.boundingBoxOfSelected()
				pointCenter.scale(1.5)
				xmin, xmax = pointCenter.xMinimum(), pointCenter.xMaximum()
				ymin, ymax = pointCenter.yMinimum(), pointCenter.yMaximum()
				points = [QgsPointXY(xmin, ymin), QgsPointXY(xmin, ymax), QgsPointXY(xmax, ymax), QgsPointXY(xmax, ymin)]
				new_feat = QgsFeature()
				new_feat.setGeometry(QgsGeometry.fromPolygonXY([points]))
				prov.addFeatures([new_feat])
				layer22.updateExtents()
				try:
					symbols = layer22.renderer().symbol()
					symbols.setColor(QColor.fromRgb(0,0,0,0))
					symbols.symbolLayer(0).setStrokeColor(QColor.fromRgb(255, 255, 255, 255))
					symbols.symbolLayer(0).setStrokeWidth(1.0)
				except:
					print(layerName)
				QgsProject.instance().addMapLayer(layer22)
				
				vLayer.removeSelection()
				iface.mapCanvas().zoomScale(1651)
				iface.mapCanvas().refreshAllLayers()
			else:
				setNextFeatureExtent()

	iface.mapCanvas().mapCanvasRefreshed.connect(snapLayer)
	setNextFeatureExtent()


Renewals_dataset = pd.read_csv('%sScripts/test2.csv' % base_dir)
rooftops = Renewals_dataset['rooftopsNearby'].as_matrix()
names = Renewals_dataset['district'].as_matrix()

createScreenshot(zip(names, rooftops))