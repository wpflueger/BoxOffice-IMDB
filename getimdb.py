# This file is to get all worldwide releases from 1989 to 2019 and their IMDB scores
# Note: Not all movies have accessable IMDB scores, which are gotten through the IMDBPY library
import imdb
from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv
from datetime import datetime

ia = imdb.IMDb()

A = []
B = []
C = []
D = []
E = []

# Get the current date
x = datetime.now()
# Set year interval
initail_Year = 1989
finish_year = 2019

year = initail_Year
# Convert Lists to single CSV file
Headings = ['Title', 'Total Earnings', 'Foriegn Earnings',
            'Year', 'IMDB']

movies = {}

date = str(x.month) + "-"+str(x.day)
csv_file = date + "IMDB_plus_boxoffice.csv"

# Loop through each year
for year in range(initail_Year, finish_year):
    url = "https://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr={}&p=.htm".format(
        year)
    print("Url: {}, year: {}".format(url, year))

    # Scrape Box Office Mojo Web Page by year
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    bo_table = soup.find_all('table')

    # Convert table from webpage to lists of Title, IMDB, Earnings, & Year
    for row in bo_table[3].find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 8:
            A.append(cells[1].find(text=True))
            movie = cells[1].find(text=True)
            print(movie)
            # Get IMDB score
            moviesearch = ia.search_movie(movie)
            # There are multiple movies with same name, so this finds the correct one and its unique movieID
            for m in moviesearch:
                mID = m.movieID
                try:
                    y = ia.get_movie(mID)['year']
                except:
                    y = 0
                if y == year and ia.get_movie(mID)['kind'] == 'movie' and ia.get_movie(mID)['title'] == movie:
                    movieID = mID
            print(movieID)
            # If it can't get the rating it will append with a -1
            # Sometimes the IMDBPY library fails to get the rating, so use "imdb from csv.py" to check the output of this file with the ratings from IMDB and replace any unknown ratings in a seperate file
            try:
                rating = ia.get_movie(movieID)['rating']
                E.append(rating)
            except:
                E.append(-1)
            # Get Domestic Revenue
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
            # get Worldwide Revenue
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
    rows = zip(A, B, C, D, E)
    # Populate CSV file each year
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(Headings)
        for row in rows:
            writer.writerow(row)
    print('CSV saved')
print('Done')
