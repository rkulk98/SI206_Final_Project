Overview:
For my final project I want to gather and analyze data about movie adaptations of popular books. In order to do so, I plan to scrape data from a Good Reads list of popular books that were turned into movies, and then access the Open Movie Database API to get data about the movie version of each of those books.

Procedure:
1.Scrape title, author, avg Good Reads rating from list of books on the GoodReads website
2.Insert into table 1 Book_Data: title, author, avg Good Reads rating, year published
3.Pass title into OMDb API and collect title, rating (PG, G, PG-13, R), imdbScore, Metacritic score, Box Office earnings
4.Insert into table 2 Movie_Adaptations: title, rating (PG, G, PG-13, R), Rotten Tomatoes Score, Metascore, Box Office earnings
5.Process data with Plotly graphs described in further detail below

Data Sources Used:
1.Good Reads list of 132 popular books that were turned into movies: https://www.goodreads.com/list/show/31274.All_Books_that_Inspired_into_Movies_?page=1
2.Open Movie Database API. This is where I will get the movie related data for each book’s on-screen adaptation. API key required:
http://www.omdbapi.com/

Accessing the Data Sources:
1.The goodreads website does not require any special procedures to access the data. I am simply crawling the site with BeautifulSoup.
2.To access data from the OMDB API, a key is required as part of the requests parameter. My key is included in the secrets.py file, which is ignored by the .gitignore file I also created.

Running the Program/User Guide:
1.Enter 'ratings' to view a Pie chart breaking down book-movie adaptations by rating (e.g PG, G, R, PG-13, Not Rated)
2.Enter 'authors' to view a Grouped bar chart comparing the top 5 authors with the highest Good Reads score, as compared to their movie’s imdbScore, and Metascore
3.Enter 'earnings' to view a Grouped bar chart comparing the imdbScore to the GoodReads rating of the movies that are ranked in the top 5 for box office earnings
4.Enter 'year' to view show grouped bar chart of all adaptations in a year of your choosing comparing Good Read’s score to Metascore and imdbScore
5.Enter 'quit' to end the program
6.Enter 'help' to view these options for reference

Important Functions:
1.scrape_and_run(): this function scrapes the title, author, and rating of the books from goodreads and then inputs that data into a csv file titled books.csv
2.init_db(): this function initializes the database with 2 tables, one for the book data and one for the movie data
3.getting_book_movie_mapping(): this function maps the id of each book (their primary key) from the Book_Data table to it's corresponding movie in the movie data table by matching the titles of the books and movies.
4.load_books(): this function, while somewhat superfluous, acts as a middle step and allows me to create a list of book objects by calling the scrape and run function, and then allowing me to not have to call the scrape and run function over and over.
