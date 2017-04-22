-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--Main table which holds the full name of the players, number of matches they have played and an unique id
DROP DATABASE IF EXISTS tournament
CREATE DATABASE tournament
\c tournament
CREATE TABLE players (id serial primary key, fullname text, matches integer default 0);
--A table to record the total wins of each player where id is the Foreign key which must match the id in players table
CREATE TABLE  wins (id serial references players, wins integer);
--CREATE VIEW standings AS SELECT players.id,players.fullname,wins.wins,players.matches FROM players LEFT JOIN wins ON wins.id=players.id ORDER BY wins.wins DESC;
