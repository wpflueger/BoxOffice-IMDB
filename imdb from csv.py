# Sometimes there is an error pulling IMDB scores, so this checks if it exists and outputs all movies with new ratings
import imdb
import csv

ia = imdb.IMDb()

A = []
B = []
C = []
D = []
E = []


# Convert Lists to single CSV file
Headings = ['Title', 'Total Earnings', 'Foriegn Earnings', 'Year', 'IMDB']

csvfile = 'Boxoffice data with IMDB.csv'
number_added = 0

with open(csvfile, mode='r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        print(row)
        print(row['Title'])
        movie = row['Title']
        A.append(row['Title'])
        B.append(row['Total Earnings'])
        C.append(row['Foriegn Earnings'])
        D.append(row['Year'])
        if float(row['IMDB']) == -1:
            try:
                movie = row['Title']
                moviesearch = ia.search_movie(movie)
                for m in moviesearch:
                    mID = m.movieID
                    year = int(row['Year'])
                    try:
                        y = ia.get_movie(mID)['year']
                    except:
                        y = 0
                    if y == year and ia.get_movie(mID)['kind'] == 'movie' and ia.get_movie(mID)['title'] == movie:
                        movieID = mID
                print(movieID)
                rating = ia.get_movie(movieID)['rating']
                E.append(rating)
                print('Rating Added')
                number_added += 1
            except Exception as e:
                print(e)
                E.append(-1)
                print('Rating not added')
        else:
            E.append(row['IMDB'])
        rows = zip(A, B, C, D, E)
        with open('output.csv', "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(Headings)
            for row in rows:
                writer.writerow(row)
        print('CSV saved with:{}'.format(movie))
print('Done. Number added: {}'.format(number_added))
