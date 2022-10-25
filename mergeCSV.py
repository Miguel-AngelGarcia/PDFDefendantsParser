#https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
import pandas as pd
import glob
import os

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/BloombergCSV/')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# setting the path for joining multiple files
#files = os.path.join("/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/BloombergCSV/", ".csv")
#files = [file for file in glob.glob("/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/BloombergCSV/*"),]

# list of merged files returned
#all_filenames = glob.glob(all_filenames)
print(all_filenames)

print("Resultant CSV after joining all CSV files at a particular location...");

# joining files with concat and read_csv
#df = pd.concat(map(pd.read_csv, files), ignore_index=True)
#print(df)


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')