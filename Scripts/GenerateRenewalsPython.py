import numpy as np
from scipy.misc import imread
from skimage import util
import cv2

import pandas as pd
from Utils import *

# Calculates the green indices of renewal areas

NDVI_LOW = -0.6
NDVI_HIGH = 0.6

GREEN_LOW = np.array([30, 0, 0])
GREEN_HIGH = np.array([70, 255, 255])

def darkmap(c):
	c = c ** (1 / 2.2)
	return 1.0 / (1.0 + np.exp(-14 * ((1-c)-0.5)))

def NDVI(imgred, imgnir):
	imgndvi = np.divide(imgnir - imgred, imgnir + imgred + np.finfo(float).eps)
	mask = np.zeros_like(imgndvi)
	mask[np.where((imgndvi > NDVI_HIGH) | (imgndvi < NDVI_LOW))] = 1.0
	return mask.mean()
	
def DMAP(imgred, imgnir):
	nmin, nmax = imgnir.min(), imgnir.max()
	rmin, rmax = imgred.min(), imgred.max()

	imgnir = (imgnir - nmin) / (nmax-nmin)
	imgred = (imgred - rmin) / (rmax - rmin)

	imgnir = np.clip(imgnir, 0, 1)
	imgred = np.clip(imgred, 0, 1)

	dred = darkmap(imgred)
	dnir = darkmap(imgnir)
	dmap = dred * dnir
	dmapmask = np.zeros_like(dmap)
	dmapmask[dmap > 0.2] = 1.0
	return dmapmask.mean()
	
	
def Greeniness(imgmap):
	imghsv = cv2.cvtColor(imgmap, cv2.COLOR_RGB2HSV)
	mask = cv2.inRange(imghsv, GREEN_LOW, GREEN_HIGH)
	return mask.mean() / 255.0
	
def fillGreen(districtName):
	global year
	imagenir = imread('../Imgs/LayersNIR/%s.png' % districtName, mode='RGB')
	imagergb = imread('../Imgs/LayersRGB %d/%s.png' % (year, districtName), mode='RGB')
	
	invnir = imagenir[:,:,0].astype('float32') / 255.0
	imgred = imagergb[:,:,0].astype('float32') / 255.0

	ndvi = NDVI(imgred, util.invert(invnir))
	greeniness = Greeniness(imagergb)
	dmap = DMAP(imgred, invnir)
	print(year, districtName, ndvi, greeniness, dmap)
	return (ndvi, greeniness, dmap)

land_numbers_dir = '%sOCR/LandNumber/' % base_dir
df = pd.read_csv('%sRenewals.csv' % data_dir)

# ADDING LAND PRICE INFO
for year in [2014, 2015, 2016, 2017, 2018]:
	lp_df = pd.read_csv('%sLand Prices %d.csv' % (data_dir, year), encoding='utf-8', dtype={'AA49': object})
	lp_df['landNum'] = lp_df['AA49'].apply(lambda x: LandNumSplit(x))

	values_df = pd.DataFrame(columns=['district', 'CurrentValue %d' % year])
	for idx, a in enumerate(df['district']):
		file = '%s%s.csv' % (land_numbers_dir, a)

		with open(file, 'r', encoding='utf-8') as f:
			renewal_df = pd.read_csv(f, header=None, names=['AA48', 'landNum'], dtype={'landNum': object})
		
		merged = pd.merge(renewal_df, lp_df, on=['AA48', 'landNum'])
		values = merged['AA16'].sum()
		values_df.loc[idx] = [a, values]

	df = pd.merge(df, values_df, on=('district'))

# ADDING GREEN INFO
for year in [2013, 2014, 2015, 2017]:
	df['ndvi %d' % year], df['greeniness %d' % year], df['dmap %d' % year] = zip(*df['district'].map(fillGreen))
df['ndvi 2016'] = 0.5 * (df['ndvi 2015'] + df['ndvi 2017'])
df['greeniness 2016'] = 0.5 * (df['greeniness 2015'] + df['greeniness 2017'])
df['dmap 2016'] = 0.5 * (df['dmap 2015'] + df['dmap 2017'])

# ADDING YEAR INFO
year_df = pd.read_csv('%sOCR/years.csv' % base_dir, encoding='utf-8', header=None, names=['district', 'date'])
df = pd.merge(df, year_df, on=('district'))
df['year'] = df['date'].apply(lambda x: x[:3])
df['e-year'] = df['year'].apply(lambda x: int(x) + 1911)

# SAVING
df.to_csv('Final.csv', index=False, encoding='utf-8')