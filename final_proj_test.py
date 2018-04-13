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
		self.assertEqual(len(result_list), 132)
		self.assertIn(('Forrest Gump'), result_list)

		statement2 = "SELECT TITLE FROM Book_Data WHERE AUTHOR = 'J.K ROWLING' "
		conn.commit()
		results2 = cur.execute(statement2)
		result_list2 = results2.fetchall()
		self.assertEqual(len(result_list2), 7)
		self.assertIn(('Harry Potter and the Chamber of Secrets'), result_list2)
		conn.close()

	def test_movie_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		statement = 'SELECT * FROM Movie_Adaptations'
		results = cur.execute(statement)
		conn.commit()
		results_list = results.fetchall()
		self.assertEqual(len(result_list), 132)
		self.assertIn(('The Lovely Bones'), result_list)

		statement2 = "SELECT TITLE FROM Movie_Adaptations WHERE TITLE NOT LIKE 'N/A' ORDER BY imdbRating DESC  "
		conn.commit()
		results2 = cur.execute(statement2)
		result_list2 = results2.fetchall()
		self.assertEqual(result_list2[0], "The Chronicles of Narnia")
		self.assertEqual((result_list2[-1]), "Alex Rider: Operation Stormbreaker")
		conn.close()

class 
