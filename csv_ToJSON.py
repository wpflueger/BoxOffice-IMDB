# This script opens the CSV files named *office.csv and CPI.csv and outputs a json file
# Use the CPI.csv file to adjust for inflation in Excel
import os
import fnmatch
import csv
import json


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*office.csv'):
        BOdata = file

# Open the CSV
movies = open(BOdata, 'r')
CPI = open('./CPI.csv', 'r')
BO_data = csv.DictReader(movies, fieldnames=('Title', 'Earnings', 'Year'))
CPI_data = csv.DictReader(CPI, fieldnames=('Year', 'Annual'))

# Dump data to json
mjson = json.dumps([row for row in BO_data])
print('mjson parsed')
cpijson = json.dumps([row for row in CPI_data])
print('cpijson parsed')

# save json to files
parsed = open('./BOjson.json', 'w')
parsed.write(mjson)
parsed = open('./CPIjson.json', 'w')
parsed.write(cpijson)

print('done')
