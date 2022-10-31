#https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
import pandas as pd
import glob
import os
import openpyxl

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/ExportFiles/')

extension = 'xlsx'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# list of merged files returned
#all_filenames = glob.glob(all_filenames)
print(all_filenames)

print("Resultant XLSX after joining all CSV files at a particular location...");

#test = pd.read_excel("TalcTen-export-20221025-170955.xlsx")

#combine all files in the list
combined_csv = pd.concat([pd.read_excel(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv_from_excel.csv", index=False, encoding='utf-8-sig')