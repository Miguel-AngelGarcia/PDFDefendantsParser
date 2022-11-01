import pandas as pd
import glob
import numpy as np
import os

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/Excel/')

talc_file = pd.read_excel('Talc_mdl.xlsx')


candidate = pd.read_csv('combined_csv.csv', usecols=['docket_number', 'defendants'])
# keep first duplicate row
candidate = candidate.drop_duplicates()

#You want to use TWO brackets, so if you are doing a VLOOKUP sort of action:
'''
pd_merged = pd.merge(mdl, bloomberg[['Plaintiff', 'LeadDefendant', 'MDLDocketNumber', 'Date Filed', 'Year', 'BloomMonth', 'BloomYear', 'Defendant Party']], on=['Plaintiff', 'LeadDefendant', 'Year'], how='left')
pd_merged = pd_merged.fillna('')
'''

mask = talc_file['Court+D'] == 'NJD'
mdl_NJD = talc_file[mask]

mdl_non_NJD = talc_file[~mask]


#Do you want to merge on NJD or non-NJD cases?
'''
pd_merged_NJD = pd.merge(mdl_NJD, candidate[['docket_number', 'defendants']],\
                         #on=['Plaintiff', 'LeadDefendant', 'Year'],\
                         left_on=['EditedDocketNumber'],\
                         right_on=['docket_number'], how='left')
pd_merged_NJD = pd_merged_NJD.fillna('')
'''

pd_merged_non_NJD = pd.merge(mdl_non_NJD, candidate[['docket_number', 'defendants']],
                             left_on=['EditedDocketNumber'], \
                             right_on=['docket_number'], how='left')
pd_merged_non_NJD = pd_merged_non_NJD.fillna('')

#pd_merged_NJD[pd_merged_NJD.duplicated(subset='EditedDocketNumber', keep=False)]

'''TEST TO SEE WHERE MULTIPLES OCCURED
vc = pd_merged_NJD.EditedDocketNumber.value_counts()
print(vc[vc >= 2])
wc = pd_merged_NJD.MDLDocketNumber.value_counts()
print(wc[wc >= 2])

THEY OCCURED in our bloomberg sheet
'''


#print(pd_merged_NJD)


'''
pd_merged_NJD.to_csv('talc_mdl_bloomberg_join2.csv', encoding='utf-8')
mdl_non_NJD.to_csv('non_NDJ_leftover.csv', encoding='utf-8')
pd_merged_non_NJD.to_csv('talc_mdl_nonNJD_bloomberg_join.csv', encoding='utf-8')
'''




