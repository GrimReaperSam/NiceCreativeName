import glob
import re
from pathlib import Path
import pandas as pd
from Scripts.Utils import *

# files = glob.glob('%s/OCR/GeoJson/*.json' % base_dir)

Renewals_dataset = pd.read_csv('%sRenewals.csv' % data_dir)
rooftops = Renewals_dataset['rooftopsNearby'].as_matrix()
names = Renewals_dataset['district'].as_matrix()
for item in zip(names, rooftops):
	current_file = '%s/OCR/GeoJson/%s.json' % (base_dir,  item[0])
	rooftops_nearby = item[1]
		
	p = Path(current_file)
	layerName = p.stem
	vLayer = QgsVectorLayer(str(p), layerName, "ogr")
	if vLayer.featureCount() != 0:
		symbols = vLayer.renderer().symbol()
		symbols.setColor(QColor.fromRgb(128 + int(127 * rooftops_nearby / 8.0), 0, 0, 255))
		symbols.symbolLayer(0).setStrokeColor(QColor.fromRgb(0,0,0,0))
		QgsProject.instance().addMapLayer(vLayer)
print("Finished")