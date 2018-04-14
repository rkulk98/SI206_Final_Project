
import requests
import csv
from bs4 import BeautifulSoup as bs
import urllib
import os
import json
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go
import secrets


class Book:
	def __init__(self, title = "No title", author= "No author", ratings = "no ratings", id = None):
		self.book_title = title
		self.book_author = author
		self.book_ratings = ratings
		self.book_id = id

	def __str__(self):
		return ("{} by {} : {}".format(self.book_title, self.book_author, self.book_ratings))

CACHE_FNAME = 'cache.json'
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}


def get_unique_key(url):
	return url


def make_request_using_cache(url):
	unique_ident = get_unique_key(url)

	if unique_ident in CACHE_DICTION:
		print("Getting cached data FOR BOOKS...")
		return CACHE_DICTION[unique_ident]


	else:
		print("Making a request for new data...")
		resp = requests.get(url)
		CACHE_DICTION[unique_ident] = resp.text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME ,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[unique_ident]


MOVIE_CACHE = 'MOVIE_CACHE.json'
try:
	cache_file = open(MOVIE_CACHE, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

# if there was no file, no worries. There will be soon!
except:
	CACHE_DICTION = {}



def omdb_params_unique_combination(baseurl, params):
	alphabetized_keys = sorted(params.keys())
	res = []
	for k in alphabetized_keys:
		res.append("{}-{}".format(k, params[k]))
	return baseurl + "_".join(res)


def make_omdb_request_using_cache(url, params):
	unique_ident = omdb_params_unique_combination(url, params)

	if unique_ident in CACHE_DICTION:
		print("Getting cached data for movies...")
		return CACHE_DICTION[unique_ident]

	else:
		print("Making a NEW request for new data...")
		resp = requests.get(url, params)
		print(resp)
		CACHE_DICTION[unique_ident] = resp.text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(MOVIE_CACHE,"w")
		fw.write(dumped_json_cache)
		fw.close()
		return CACHE_DICTION[unique_ident]

def scrape_and_run():
	all_books = []
	titles_list = []
	authors_list = []
	ratings_list = []
	for page in range(1 ,3):
		page = make_request_using_cache("https://www.goodreads.com/list/show/31274.All_Books_that_Inspired_into_Movies_?page={}".format(str(page)))
		soup = bs(page, 'html.parser')

		all_listings = soup.find_all('title')

		books_listings = soup.find_all('tr')
		for x in books_listings:
			tr_num = books_listings.index(x)
			tr = x
			cells = tr.find_all('td')
			book_info = cells[2]
			titles_a_class = book_info.find_all('a', class_='bookTitle')
			for t in titles_a_class:
				title = t.find(itemprop = "name").text
				titles_list.append(title.split("(")[0])
			authors_a_class = book_info.find_all('a', class_='authorName')
			for a in authors_a_class:
				author = a.find(itemprop = "name").text
				authors_list.append(author)

			rating_info = book_info.find_all('span', {"class": "greyText smallText uitext"})
			# print(rating_info)
			# HOW DO I GET THE RATING INFORMATION AND THEN HOW DO I BREAK IT UP???
			for info in rating_info:
				average_rating = info.get_text()
				average_rating.split()
				ratings_list.append(average_rating[2:6])
			# ratings_list.append(info[9].text)

	for t, a, r in zip(titles_list, authors_list, ratings_list):
		new_book = Book(t, a, r)
		all_books.append(new_book)


	#



	with open('books.csv', 'w' ,newline='') as csvfile:
		fieldnames = ['title', 'author', 'avg. rating']
		csv_write = csv.DictWriter(csvfile, fieldnames=fieldnames)
		books_save = 0

		for a_book in all_books:

			try:

				# title_name = t.get_text()
				# author_name = a.get_text()
				# rating_stuff = p.get_text()
				# print(title_name, author_name, published_info)

				csv_write.writerow({
					'title': a_book.book_title.split("(")[0],
					'author': a_book.book_author,
					'avg. rating': a_book.book_ratings})
				# '# of ratings': rating_stuff.split()[4],
				# 'year published': rating_stuff.split()[8] }

				books_save += 1
			## error handelling for long file names
			except:
				print("error")

		print("{} books saved.".format(books_save)) # books count feedback
	return(all_books)


def getOMDBdata(title, book_id):
	response = make_omdb_request_using_cache('http://www.omdbapi.com', params = {'apikey' : secrets.api_key ,'t' :title })
	movie_data = json.loads(response)
	# using book_id from insert_omdb_data
	movie_data['book_id'] = book_id;
	adaptations = []
	return(movie_data)



DBNAME = 'book_movie_data.db'
BOOKSCSV = 'books.csv'

def init_db():

	print('Creating Database')
	try:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
	except:
		print("Error with db")

	statement_json = '''
		DROP TABLE IF EXISTS 'Movie_Adaptations';
	'''
	cur.execute(statement_json)
	conn.commit()

	statement_json = '''
		CREATE TABLE 'Movie_Adaptations' (
		'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'Title' TEXT NOT NULL,
		'Year' INTEGER NOT NULL,
		'Rating' TEXT NOT NULL,
		'imdbRating' Integer NOT NULL,
		'MetaScore' Integer NOT NULL,
		'BoxOffice' Integer NOT NULL,
		'Book_ID' Integer NOT NULL
		 );
	 '''
	cur.execute(statement_json)
	conn.commit()

	statement_csv = ''' DROP TABLE IF EXISTS 'Book_Data'; '''
	cur.execute(statement_csv)
	conn.commit()

	statement_csv = '''
		CREATE TABLE 'Book_Data' (
		'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'Title' TEXT NOT NULL,
		'Author' TEXT NOT NULL,
		'AvgRating' Integer NOT NULL
		 );
	 '''
	cur.execute(statement_csv)
	conn.commit()
	conn.close()

def insert_csv_data():
	try:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
	except:
		print("Error inserting CSV data")

	print("Inserting csv data")

	with open(BOOKSCSV) as csvDataFile:
		csvReader = csv.reader(csvDataFile)


		for row in csvReader:
			insertion = (None, row[0], row[1], row[2])
			statement_csv = 'INSERT INTO "Book_Data" '
			statement_csv += 'VALUES (?, ?, ?, ?) '
			cur.execute(statement_csv, insertion)
			conn.commit()
		conn.close()

def getting_book_movie_mapping():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query = "SELECT * FROM Book_Data"
	cur.execute(query)
	books = {}
	for book in cur:
		book_id = book[0]
		title = book[1]
		books[title] = book_id
	# print(books)
	conn.commit()


	for x in books:
		a_book = x
		id = books[x]
		insert = (id, a_book)
		statement = 'UPDATE Movie_Adaptations '
		statement += 'SET Book_ID =? '
		statement += 'WHERE Book_ID =? '
		cur.execute(statement ,insert)
		conn.commit()

	conn.close()

def insert_omdb_data():
	try:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
	except:
		print("Error inserting OMDB data")
	# The primary key book_id is an auto number and the value of book_id will only be known after the book
	# data has been inserted. So instead of using data from the function scrape_and_run
	# an additional function load_books below performs the same function
	# using book_id to perform inserts below
	testing_data_stuff = load_books()
	final_adaptation_list = []
	for book in testing_data_stuff:
		# Using the book_id to insert the data into the movies_adaptation table
		# passing book_id also to getOMDBdata
		final_adaptation_list.append(getOMDBdata(book.book_title, book.book_id))
	# print(final_adaptation_list)
	# print("{} ADAPTATIONS IN THIS LIST".format(len(final_adaptation_list)))
	for dic in final_adaptation_list:
		book_id = ""
		# print('dic. book_id ', dic.get("book_id", None))
		insertion = (None, dic.get("Title" ,"N/A"),dic.get("Year" ,"N/A"), dic.get("Rated" ,"N/A"),
					 dic.get("imdbRating" ,"N/A"), dic.get("Metascore" ,"N/A"),
					 dic.get("BoxOffice" ,"N/A"), dic.get("book_id", None))

		statement_json = 'INSERT INTO "Movie_Adaptations" '
		statement_json += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?) '
		cur.execute(statement_json, insertion)
	conn.commit()
	conn.close()
# def get_movie_data():

def load_books():
	all_books = []
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query = "SELECT Id, Title, Author, AvgRating FROM Book_Data"
	cur.execute(query)
	books = {}
	for book in cur:
		new_book = Book(book[1], book[2], book[3], book[0])
		all_books.append(new_book)
	return(all_books)
	conn.commit()
	conn.close()

def pie_chart():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query = "SELECT COUNT(*) FROM Movie_Adaptations GROUP BY Rating HAVING RATING NOT LIKE 'N/A' "
	labels = ['R','PG-13','G','PG', 'NOT RATED', 'PASSED']
	values = []
	cur.execute(query)
	for row in cur:

		values.append(row)

	trace = go.Pie(labels=labels, values=values)

	py.plot([trace], filename='basic_pie_chart')
	conn.commit()
	conn.close()

def top5_authors():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query1 = "SELECT Title, Author FROM Book_Data group by author ORDER BY AvgRating DESC LIMIT 5"

	top5_titles = []
	top5_authors = []
	cur.execute(query1)
	conn.commit()

	imdb_ratings = []
	meta_ratings = []
	for row in cur:
		top5_titles.append(row[0])
		top5_authors.append(row[1])
	for title in top5_titles:
		query2 = "SELECT imdbRating, MetaScore FROM Movie_Adaptations WHERE Title = '{}' ".format(title)
		cur.execute(query2)
		conn.commit()
		for row in cur:
			imdb_ratings.append(row[0]*10)
			meta_ratings.append(row[1])

	trace1 = go.Bar(
	x= top5_authors,
	y=imdb_ratings,
	name='IMDB Rating'
	)
	trace2 = go.Bar(
		x= top5_authors,
		y=meta_ratings,
		name='Metascore Rating'
	)


	data = [trace1, trace2]
	layout = go.Layout(
		barmode='group'
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='grouped-bar-1')
	# conn.commit()
	conn.close()

def top5_movies():

	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query1 = "SELECT Title, BoxOffice, imdbRating FROM Movie_Adaptations GROUP BY TITLE HAVING BoxOffice NOT LIKE 'N/A' ORDER BY BoxOffice DESC LIMIT 5"

	top5_titles = []
	cur.execute(query1)
	conn.commit()

	gr_ratings = []
	imdb_ratings = []
	for row in cur:
		top5_titles.append(row[0])
		imdb_ratings.append(row[2])

	for title in top5_titles:

		query2 = 'SELECT AvgRating FROM Book_Data WHERE Title = "{}" '.format(title)

		cur.execute(query2)
		conn.commit()
		for row in cur:
			gr_ratings.append(row[0])


	trace1 = go.Bar(
	x= top5_titles,
	y=imdb_ratings,
	name='IMDB Rating'
	)
	trace2 = go.Bar(
		x= top5_titles,
		y=gr_ratings,
		name='GoodReads Rating'
	)


	data = [trace1, trace2]
	layout = go.Layout(
		barmode='group'
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='grouped-bar-2')
	# conn.commit()
	conn.close()

def score_by_year():
	year = input("Ask for a year: ")
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	query1 = "SELECT Title, MetaScore, imdbRating FROM Movie_Adaptations WHERE Year = '{}' ".format(year)

	titles = []
	meta_ratings = []
	imdb_ratings = []
	cur.execute(query1)
	conn.commit()

	gr_ratings = []

	for row in cur:
		titles.append(row[0])
		meta_ratings.append(row[1])
		imdb_ratings.append(row[2]*10)

	for title in titles:

		query2 = 'SELECT AvgRating FROM Book_Data WHERE Title = "{}" '.format(title)

		cur.execute(query2)
		conn.commit()
		for row in cur:
			gr_ratings.append(row[0]*20)


	trace1 = go.Bar(
	x= titles,
	y=imdb_ratings,
	name='IMDB Rating'
	)
	trace2 = go.Bar(
		x= titles,
		y=meta_ratings,
		name='MetaScore Rating'
	)
	trace3 = go.Bar(
		x= titles,
		y=gr_ratings,
		name='GoodReads Rating'
	)

	data = [trace1, trace2, trace3]
	layout = go.Layout(
		barmode='group'
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='grouped-bar-2')
	# conn.commit()
	conn.close()

if __name__ == '__main__':

	init_db()
	testing_data_stuff = scrape_and_run()
	insert_csv_data()

	insert_omdb_data()
	getting_book_movie_mapping()

	command = input("Enter a command or help for more options. Enter quit to terminate program: ")
	while command != 'quit':
		if command == "ratings":
			pie_chart()
		if command == "authors":
			top5_authors()
		if command == "earnings":
			top5_movies()
		if command == "year":
			score_by_year()
		if command == "help":
			statement1 = "1.)Enter 'ratings' to view a Pie chart breaking down book-movie adaptations by rating "
			statement2 = "2.)Enter 'authors' to view a Grouped bar chart comparing the top 5 authors with the highest Good Reads score, as compared to their movie’s imdbScore, and Metascore "
			statement3 = "3.)Enter 'earnings' to view a Grouped bar chart comparing the imdbScore to the GoodReads rating of the movies that are ranked in the top 5 for box office earnings"
			statement4 = "4.)Enter 'year' to view show grouped bar chart of all adaptations in a year of your choosing comparing Good Read’s score to Metascore and imdbScore"
			print(statement1 + "\n" + statement2 + "\n" + statement3 + "\n" + statement4)
		else:
			print("Sorry, that command appears to be invalid. Enter 'help' for a list of valid commands.")
		command = input("Enter a command or enter quit to terminate program: ")
	print("Bye!")

# final_adaptation_list = []
# for book in testing_data_stuff:
# 	final_adaptation_list.append(getOMDBdata(book.book_title))
# print(final_adaptation_list)
# print("{} adaptations".format(len(final_adaptation_list)))
