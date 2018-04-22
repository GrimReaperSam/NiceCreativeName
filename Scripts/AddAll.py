import glob
import re
from pathlib import Path

base_dir = 'C:/Users/Fayez Lahoud/Desktop/Academic/Courses/Personal Interaction Studio/NiceCreativeName/'

files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)
for f in files:
	p = Path(f)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		symbols = vLayer.renderer().symbol()
		symbols.setColor(QColor.fromRgb(50, 50, 250))
		QgsProject.instance().addMapLayer(vLayer)
print("Finished")