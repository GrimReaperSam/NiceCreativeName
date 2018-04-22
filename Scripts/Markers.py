import sys
import pandas as pd
from Scripts.Utils import *

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
