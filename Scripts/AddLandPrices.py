import pandas as pd
from Utils import *

Renewals_dataset = pd.read_csv('%sRenewals.csv' % data_dir)

lp_df = pd.read_csv('%sLandPrices.csv' % data_dir, 
	encoding='utf-8', dtype={'AA49': object})
lp_df['landNum'] = lp_df['AA49'].apply(lambda x: LandNumSplit(x))
with open('%sOCR/LandNumber/士林區B0482.csv' % base_dir, 'r', encoding='utf-8') as f:
	renewal_df = pd.read_csv(f, header=None, names=['AA48', 'landNum'])
	
merged = pd.merge(renewal_df, lp_df, on=['AA48', 'landNum'])
