import unittest
from final_proj import *


class TestDatabase(unittest.TestCase):
	def test_book_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		statement = 'SELECT * FROM Book_Data'
		results = cur.execute(statement)
		conn.commit()
		results_list = results.fetchall()
		self.assertEqual(len(results_list), 132)
		self.assertIn(('The Help'), results_list[29])

		statement2 = "SELECT Title FROM Book_Data Where Author = 'J.K. Rowling' "

		cur.execute(statement2)
		results_list2 = []
		for row in cur:
			results_list2.append(row[0])
		# results_list2 = results2.fetchall()
		self.assertEqual(len(results_list2), 7)
		self.assertIn(('Harry Potter and the Chamber of Secrets '), results_list2)
		conn.commit()
		conn.close()

	def test_movie_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		statement = 'SELECT * FROM Movie_Adaptations'
		results = cur.execute(statement)
		conn.commit()
		results_list = results.fetchall()
		self.assertEqual(len(results_list), 132)
		self.assertIn(('The Kite Runner'), results_list[18])

		statement2 = "SELECT TITLE FROM Movie_Adaptations WHERE TITLE NOT LIKE 'N/A' ORDER BY imdbRating DESC  "
		conn.commit()
		cur.execute(statement2)
		result_list2 =[]
		for row in cur:
			result_list2.append(row[0])
		self.assertEqual(result_list2[0], "The Chronicles of Narnia")
		self.assertEqual((result_list2[-1]), "Alex Rider: Operation Stormbreaker")
		conn.close()

class TestDataProcessing(unittest.TestCase):
	def test_plotly_data_pie(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		query = "SELECT COUNT(*) FROM Movie_Adaptations GROUP BY Rating HAVING RATING NOT LIKE 'N/A' "
		values = []
		cur.execute(query)
		for row in cur:
			values.append(row)
		self.assertTrue(len(values)>0)
		self.assertTrue(len(values)<132)
		conn.commit()
		conn.close()

	def test_plotly_data_authors(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		query1 = "SELECT Title, Author FROM Book_Data group by author ORDER BY AvgRating DESC LIMIT 5"

		top5_titles = []
		top5_authors = []
		cur.execute(query1)
		conn.commit()

		for row in cur:
			top5_titles.append(row[0])
			top5_authors.append(row[1])

		self.assertEqual(len(top5_titles),5)
		self.assertEqual(len(top5_authors),5)
		self.assertTrue(top5_authors[0], "Dodie Smith")
		conn.close()

	def test_plotly_data_movies(self):
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

		self.assertTrue(top5_titles[0], "The Maze Runner")
		self.assertEqual(len(top5_titles),5)
		conn.close()

unittest.main(verbosity=2)
