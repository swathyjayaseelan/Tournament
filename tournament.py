#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        c = db.cursor()
        return db, c
    except:
        print("<error message>")
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute("UPDATE players SET matches=0")
    c.execute("UPDATE wins SET wins=0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute("TRUNCATE TABLE players CASCADE")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    c.execute("SELECT COUNT(*) FROM players")
    result = c.fetchone()
    return result[0]
    db.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    db.cursor()
    c.execute("INSERT INTO  players (fullname,matches)" +
              "VALUES (%s,0) RETURNING id;", (name, ))
    for row in c.fetchall():
        result = row[0]
        c.execute("INSERT INTO wins (id,wins) VALUES (%s,0)", (result, ))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player
    in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    db.cursor()
    c.execute("SELECT players.id,players.fullname,wins.wins,players.matches" +
              "FROM players LEFT JOIN wins ON players.id=wins.id" +
              "ORDER BY wins.wins DESC")
    result = c.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    db.cursor()
    c.execute("UPDATE players SET matches=matches+1 WHERE id=%s", (winner, ))
    c.execute("UPDATE wins SET wins=wins+1 WHERE id=%s", (winner, ))
    c.execute("UPDATE players SET matches=matches+1 WHERE id=%s", (loser, ))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, c = connect()
    db.cursor()
    playerStandings()
    c.execute("CREATE VIEW standings AS SELECT" +
              "players.id,players.fullname,wins.wins,players.matches FROM" +
              "players LEFT JOIN wins on wins.id=players.id" +
              "ORDER BY wins.wins DESC ")
    c.execute("SELECT COUNT(*) FROM standings")
    '''Find the total number of players in the table'''
    for row in c.fetchall():
        total = row[0]
    i = 0
    result = []
    '''Iterate through the rows in the table and pair two players'''
    while total > 0:
        c.execute("SELECT id,fullname FROM standings LIMIT 2 OFFSET %s", (i, ))
        i = i + 2
        '''create tuples'''
        res = reduce(list.__add__, map(list, c.fetchall()))
        total = total-2
        '''Add the tuples to a list'''
        result.append(res)
    db.close()
    return result

