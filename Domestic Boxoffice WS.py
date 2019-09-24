# This file is to get all domestic releases in the US: Total US revenue, Opening weekend, Open Date, & Close Date for all movies from 1980-2019
# Note:There is no close date data for movies that are from before 2002

from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv
from datetime import datetime

A = []
B = []
C = []
D = []
E = []

# Get the current date
x = datetime.now()
# Set year interval
initail_Year = 1980
finish_year = 2020

year = initail_Year
url = "https://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=2018&p=.htm"

for year in range(initail_Year, finish_year):
    for i in range(1, 11):
        url = "https://www.boxofficemojo.com/yearly/chart/?page={}&view=releasedate&view2=domestic&yr={}&p=.htm".format(
            i, year)
        print("Url: {}, i: {}, year: {}".format(url, i, year))
        # Scrape Box Office Mojo Web Page
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        bo_table = soup.find_all('table')
        # Convert table from webpage to lists of Title, Earnings, & Year
        for row in bo_table[4].find_all("tr"):
            cells = row.find_all("td")
            # Before 2002 there are no close dates, therefore the len needs to be 8
            if year < 2002:
                table_len = 8
            else:
                table_len = 9
            if len(cells) == table_len:
                A.append(cells[1].find(text=True))
                oldstr = cells[3].find(text=True)
                newstr = oldstr.replace('$', "")
                B.append(newstr)
                oldstr = cells[5].find(text=True)
                newstr = oldstr.replace('$', "")
                C.append(newstr)
                oldstr = cells[7].find(text=True)
                newstr = str(oldstr) + "/" + str(year)
                # print(newstr)
                strdate1 = newstr
                D.append(newstr)
                if year >= 2002:
                    oldstr = cells[8].find(text=True)
                    newstr = str(oldstr) + "/" + str(year)
                    E.append(newstr)
                else:
                    E.append("NA")

# Convert Lists to single CSV file
Headings = ['Title', 'Earnings', 'Opening Weekend',
            'Opening Date', 'Close Date']

movies = {}

date = str(x.month) + "-"+str(x.day)
csv_file = date+" boxoffice.csv"

rows = zip(A, B, C, D, E)

# Populate CSV file
with open(csv_file, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(Headings)
    for row in rows:
        writer.writerow(row)
