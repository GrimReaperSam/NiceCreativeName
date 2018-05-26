import sys
import pandas as pd
from Scripts.Utils import *

# Add all illegal rooftops on the map

csv_dir = data_dir + 'output.csv'

dataset = pd.read_csv(csv_dir)
coords = [tuple(x) for x in dataset[['Lng','Lat']].values]

canvas = qgis.utils.iface.mapCanvas()

for c in coords:
	m = QgsVertexMarker(canvas)
	m.setCenter(QgsPointXY (*c))
	m.setColor(QColor(255, 0, 0))
	m.setIconSize(5)
	m.setPenWidth(5)
	m.setIconType(QgsVertexMarker.ICON_CIRCLE)

	
# Add all renewal areas on the map
Renewals_dataset = pd.read_csv('%sRenewals.csv' % data_dir)
names = Renewals_dataset['district'].as_matrix()
for item in names:
	current_file = '%s/OCR/GeoJson/%s.json' % (base_dir,  item)
		
	p = Path(current_file)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		symbols = vLayer.renderer().symbol()
		symbols.setColor(QColor.fromRgb(256, 0, 0, 255))
		symbols.symbolLayer(0).setStrokeColor(QColor.fromRgb(0,0,0,0))
		QgsProject.instance().addMapLayer(vLayer)

print("Finished")