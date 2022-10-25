import pandas as pd
import glob
import numpy as np
import os

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/')

mdl = pd.read_csv('MDLComplaintStateInfo.csv', usecols=['CaseName', 'Plaintiff', 'LeadDefendant', 'EditedDocketNumber', 'StartDate', 'Year', 'Court+D'])
mdl['MDLMonth'] = pd.to_datetime(mdl['StartDate']).dt.month
mdl['MDLYear'] = pd.to_datetime(mdl['StartDate']).dt.year
# keep first duplicate row
mdl = mdl.drop_duplicates()

bloomberg = pd.read_csv('BloomberComplaintMDLInfo.csv', usecols=['Title', 'Plaintiff', 'LeadDefendant',\
                                                        'MDLDocketNumber', 'Year', 'Date Filed', 'Defendant Party'])
bloomberg['BloomMonth'] = pd.to_datetime(bloomberg['Date Filed']).dt.month
bloomberg['BloomYear'] = pd.to_datetime(bloomberg['Date Filed']).dt.year
# keep first duplicate row
bloomberg = bloomberg.drop_duplicates()

#You want to use TWO brackets, so if you are doing a VLOOKUP sort of action:
'''
pd_merged = pd.merge(mdl, bloomberg[['Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Date Filed', 'Year', 'BloomMonth', 'BloomYear', 'Defendant Party']], on=['Plaintiff', 'LeadDefendant', 'Year'], how='left')
pd_merged = pd_merged.fillna('')
'''
#pd_merged['Year']=pd_merged['Year'].astype('Int64')
#pd_merged['BloomMonth']=pd_merged['BloomMonth'].astype('Int64')
#pd_merged['BloomYear']=pd_merged['BloomYear'].astype('Int64')

mask = mdl['Court+D'] == 'NJD'
mdl_NJD = mdl[mask]

mdl_non_NJD = mdl[~mask]

pd_merged_NJD = pd.merge(mdl_NJD, bloomberg[['Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Date Filed', 'Year', 'BloomMonth', 'BloomYear', 'Defendant Party']],\
                         #on=['Plaintiff', 'LeadDefendant', 'Year'],\
                         left_on=['Plaintiff', 'LeadDefendant', 'Year', 'EditedDocketNumber'],\
                         right_on=['Plaintiff', 'LeadDefendant', 'Year', 'MDLDocketNumber'], how='left')
pd_merged_NJD = pd_merged_NJD.fillna('')

pd_merged_non_NJD = pd.merge(mdl_non_NJD, bloomberg[['Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Date Filed', 'Year', 'BloomMonth', 'BloomYear', 'Defendant Party']],\
                         on=['Plaintiff', 'LeadDefendant', 'Year'], how='left')
                         #left_on=['Plaintiff', 'LeadDefendant', 'Year', 'EditedDocketNumber'],\
                         #right_on=['Plaintiff', 'LeadDefendant', 'Year', 'MDLDocketNumber'], how='left')
pd_merged_non_NJD = pd_merged_non_NJD.fillna('')


pd_merged_non_NJD['Match'] = np.where((pd_merged_non_NJD['MDLMonth'] == pd_merged_non_NJD['BloomMonth']) , 'Good', 'Uncertain')

group = pd_merged_non_NJD.groupby('EditedDocketNumber')
pd_merged_non_NJD['GoodCheck'] = (group['Match'].transform(lambda x: x.eq('Good').any()))

#pd_merged_NJD[pd_merged_NJD.duplicated(subset='EditedDocketNumber', keep=False)]

'''TEST TO SEE WHERE MULTIPLES OCCURED
vc = pd_merged_NJD.EditedDocketNumber.value_counts()
print(vc[vc >= 2])
wc = pd_merged_NJD.MDLDocketNumber.value_counts()
print(wc[wc >= 2])

THEY OCCURED in our bloomberg sheet
'''


print(pd_merged_NJD)

pd_merged_NJD.to_csv('talc_mdl_bloomberg_join2.csv', encoding='utf-8')

mdl_non_NJD.to_csv('non_NDJ_leftover.csv', encoding='utf-8')


pd_merged_non_NJD.to_csv('talc_mdl_nonNJD_bloomberg_join.csv', encoding='utf-8')