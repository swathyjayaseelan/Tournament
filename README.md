# Tournament_database

Udacity-tournament-database is a simple database project completed for Udacity's full-stack nanodegree program. 
It is a database backed application that uses PostgreSQL database to record the players, matches and winners of a Swiss-based non-elimination tournament.
Python is used to query the database and pair the players for matches based on the number of wins of each player

**Required files and dependencies**

Python V2.* and above and PostgreSQL database are required

**Files included**
1. tournament.sql     - to set up the database scheme
2. tournament.py      - to provide access to the database via a library of functions which can add, delete or query data in the database to another python program
3. tournament_test.py - client program to test the implementation of the functions written in tournament.py

**How to run the project**
1. Clone the github repo and download the zip files into your local computer
2. Log into the web server via SSH
3. Log into the PostgreSQL database "psql"
4. To intialise the tables run "/i tournament.sql"
5. Log out of the database with "\q" 
6. Run the test file to execute the suite of unit tests "python tournament_test.py"
