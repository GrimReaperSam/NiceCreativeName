import sys
import pandas as pd

base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/Project/'

csv_dir = base_dir + 'Data/output.csv'

dataset = pd.read_csv(csv_dir)
coords = [tuple(x) for x in dataset[['Address', 'Lng','Lat']].values]


canvas = qgis.utils.iface.mapCanvas()

for c in coords:
	m = QgsVertexMarker(canvas)
	m.setCenter(QgsPointXY (*c[1:]))
	m.setColor(QColor(255, 0, 0))
	m.setIconSize(5)
	m.setPenWidth(5)
	m.setIconType(QgsVertexMarker.ICON_CIRCLE)
	
def remove_markers():
	scene = canvas.scene()
	vertex_items = [i for i in scene.items() if issubclass(type(i), qgis.gui.QgsVertexMarker)]
	for ver in vertex_items:
		if ver in scene.items():
			scene.removeItem(ver)
	canvas.refresh()