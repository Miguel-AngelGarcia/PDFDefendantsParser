#https://stackoverflow.com/questions/43451580/remove-first-4-lines-in-multiple-csv-files-python
import glob
import os

os.chdir('/Users/miguelgarcia/Desktop/Work/LitigationTracking/Talc/BloombergCSV/')

myfiles = glob.glob('*.csv')
for file in myfiles:
    print("filename: ", file)
    lines = open(file).readlines()
    open(file, 'w').writelines(lines[2:])


#add something that takes file, copies, and adds it to 'copy' folder before writing
#this way we have new file and original file