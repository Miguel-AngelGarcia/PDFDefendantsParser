import pandas as pd
import glob
import numpy as np
import os

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/')

mdl = pd.read_csv('MDLComplaintStateInfo.csv', usecols=['CaseName', 'Plaintiff', 'LeadDefendant', 'EditedDocketNumber', 'StartDate', 'Year', 'Court+D'])
mdl['MDLMonth'] = pd.to_datetime(mdl['StartDate']).dt.month
mdl['MDLYear'] = pd.to_datetime(mdl['StartDate']).dt.year

bloomberg = pd.read_csv('BloomberComplaintMDLInfo.csv', usecols=['Title', 'Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Year', 'Date Filed', 'Defendant Party'])
bloomberg['BloomMonth'] = pd.to_datetime(bloomberg['Date Filed']).dt.month
bloomberg['BloomYear'] = pd.to_datetime(bloomberg['Date Filed']).dt.year

#You want to use TWO brackets, so if you are doing a VLOOKUP sort of action:
pd_merged = pd.merge(mdl, bloomberg[['Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Date Filed', 'Year', 'BloomMonth', 'BloomYear', 'Defendant Party']], on=['Plaintiff', 'LeadDefendant', 'Year'], how='left')
pd_merged = pd_merged.fillna('')
#pd_merged['Year']=pd_merged['Year'].astype('Int64')
#pd_merged['BloomMonth']=pd_merged['BloomMonth'].astype('Int64')
#pd_merged['BloomYear']=pd_merged['BloomYear'].astype('Int64')

pd_merged['Match'] = np.where((pd_merged['MDLMonth'] == pd_merged['BloomMonth']) | (pd_merged['EditedDocketNumber'] == pd_merged['MDLDocketNumber']) , 'Good', 'Uncertain')
group = pd_merged.groupby('EditedDocketNumber')

pd_merged['GoodCheck'] = (group['Match'].transform(lambda x: x.eq('Good').any()))



print(pd_merged)

pd_merged.to_csv('talc_mdl_bloomberg_join2.csv', encoding='utf-8')