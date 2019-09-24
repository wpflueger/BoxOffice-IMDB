# This file is to get all worldwide box office earnings from 1989-2019
# Note: There are some movies with no domestic or foreign earnings

from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv
from datetime import datetime
import imdb

ia = imdb.IMDb()

A = []
B = []
C = []
D = []

# Get the current date
x = datetime.now()
# Set year interval
initail_Year = 1989
finish_year = 2020

year = initail_Year

for year in range(initail_Year, finish_year):
    url = "https://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr={}&p=.htm".format(
        year)
    print("Url: {}, year: {}".format(url, year))
    # Scrape Box Office Mojo Web Page
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    bo_table = soup.find_all('table')
    # Convert table from webpage to lists of Title, Earnings, & Year
    for row in bo_table[3].find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 8:
            A.append(cells[1].find(text=True))
            oldstr = cells[3].find(text=True)
            newstr = oldstr.replace('$', "")
            newstr = newstr.replace(',', "")
            newstr = newstr.replace('n/a', "0")
            if newstr.find('k') == -1:
                newint = float(newstr) * 1000000
                B.append(newint)
            else:
                newstr2 = newstr.replace('k', "")
                newint = float(newstr2) * 1000
                B.append(newint)
            oldstr = cells[4].find(text=True)
            newstr = oldstr.replace('$', "")
            newstr = newstr.replace(',', "")
            newstr = newstr.replace('n/a', "0")
            if newstr.find('k') == -1:
                newint = float(newstr) * 1000000
                C.append(newint)
            else:
                newstr2 = newstr.replace('k', "")
                newint = float(newstr2) * 1000
                C.append(newint)
            D.append(year)


# Convert Lists to single CSV file
Headings = ['Title', 'Total Earnings', 'Foriegn Earnings',
            'Year']

movies = {}

date = str(x.month) + "-"+str(x.day)
csv_file = date + " WW boxoffice.csv"

rows = zip(A, B, C, D)

# Populate CSV file
with open(csv_file, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(Headings)
    for row in rows:
        writer.writerow(row)
