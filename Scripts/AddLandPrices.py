import pandas as pd
from Utils import *

land_numbers_dir = '%sOCR/LandNumber/' % base_dir
Renewals_dataset = pd.read_csv('%sRenewals.csv' % data_dir)

lp_df = pd.read_csv('%sLandPrices.csv' % data_dir, 
	encoding='utf-8', dtype={'AA49': object})
lp_df['landNum'] = lp_df['AA49'].apply(lambda x: LandNumSplit(x))

values_df = pd.DataFrame(columns=['district', 'CurrentValue', 'LandValue'])
for idx, a in enumerate(Renewals_dataset['district']):
	file = '%s%s.csv' % (land_numbers_dir, a)

	with open(file, 'r', encoding='utf-8') as f:
		renewal_df = pd.read_csv(f, header=None, names=['AA48', 'landNum'], dtype={'landNum': object})
	
	merged = pd.merge(renewal_df, lp_df, on=['AA48', 'landNum'])
	values = merged[['AA16', 'AA17']].sum()
	values_df.loc[idx] = [a, values[0], values[1]]
	
Renewals_dataset = pd.merge(Renewals_dataset, values_df, on=('district'))
Renewals_dataset.to_csv('%sRenewals-Prices.csv' % data_dir, index=False, encoding='utf-8')
