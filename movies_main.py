"""
CSCI-140/242

A program that demonstrates custom sorting a list of dataclass objects by
several fields.

Author: Miles Sopchak
"""

import os.path
import sys
from dataclasses import dataclass
import time
from typing import List, TextIO

@dataclass
class Movie:
    """a dataclass to represent basic information about a Movie"""
    tconst: str
    titleType: str
    primaryTitle: str
    startYear: int
    runTimeMinutes: int
    genres: str

    def print(self):
        """prints the information stored in the Movie dataclass to the console"""
        return 'Identifier: ' + self.tconst + ', Title: ' + self.primaryTitle + ', Type: ' + self.titleType + ', Year: ' + str(self.startYear) + ', Runtime: ' + str(self.runTimeMinutes) + ', Genres: ' + self.genres

@dataclass
class Rating:
    """a dataclass to represent basic information about ratings for a Movie"""
    tconst: str
    averageRating: float
    numVotes: int

    def print(self):
        """prints the information stored in the Rating dataclass to the console"""
        print('\tRATING: Identifier: ' + self.tconst + ', Rating: ' + str(self.averageRating) + ', Votes: ' + str(
            self.numVotes))

def getInputFiles() -> tuple[TextIO, TextIO, str]:
    """
    reads the run configuration parameters and opens the correct data files
    :return: 3 variables:
        file1 contains all the basic movie information,
        files2 contains all the ratings information for the movies
        size describes if file1 and file2 are the large or small variants
    """
    try:
        if (sys.argv[1] == 'small'):
            size = 'small'
            file1 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/small.basics.tsv', encoding="utf-8")
            file2 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/small.ratings.tsv', encoding="utf-8")
        else:
            file1 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/title.basics.tsv', encoding="utf-8")
            file2 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/title.ratings.tsv', encoding="utf-8")
            size = 'title'
    except:
        file1 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/title.basics.tsv', encoding="utf-8")
        file2 = open(sys.argv[0][0:len(sys.argv[0]) - 18] + 'data/title.ratings.tsv', encoding="utf-8")
        size = 'title'
    return file1, file2, size


def readMovies(file):
    """
    reads a file of basic movie information into a dic
    :param file: the file to be red
    :return: dic of tconst: Movie
    """
    movies = {}
    run = True
    for line in file:
        if (run):
            run = False
        else:
            line = line.split('\t')
            if (line[4] == '0'):
                if (line[5] == "\\N"):
                    startYear = 0
                else:
                    startYear = int(line[5])
                if (line[7] == "\\N"):
                    runTimeMinuets = 0
                else:
                    runTimeMinuets = int(line[7])
                if (line[8] == "\\N"):
                    genres = None
                else:
                    genres = line[8][0:-1]

                movies[line[0]] = Movie(line[0], line[1], line[2], startYear, runTimeMinuets, genres)
    return movies


def readRatings(file, movies):
    """
    reads a file of movie rating information into a dic
    :param file: the file to be red
    :param movies: dic of tconst: Movie needed to get tconst
    :return: dic of tconst: Rating
    """
    ratings = {}
    run = True
    for line in file:
        if (run):
            run = False
        else:
            line = line.split('\t')
            if line[0] in movies:
                ratings[line[0]] = Rating(line[0], line[1], line[2][0:-1])
    return ratings


def LOOKUP(tconst, movies, ratings):
    """
    finds the Movie and Rating dataclass with the key tconst and prints them out
    :param tconst: key for movies, and ratings dictionarys
    :param movies: dic of tconst: Movie
    :param ratings: dic of tconst: Rating
    :return: None
    """
    print('processing: LOOKUP ' + tconst)
    start = time.perf_counter()
    if tconst in movies:
        m = movies[tconst]
        print('\tMOVIES: ' + m.print())
    else:
        print('\tMovie not found!')
    start = time.perf_counter()
    if tconst in ratings:
        r = ratings[tconst]
        r.print()
    else:
        print('\tRating not found!')
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')


def CONTAINS(titleType, words, movies):
    """
    searches movies for a Movie with a specified titleType that has a title that contains the string words and
        prints them out
    :param titleType: attribute of Movie dataclass
    :param words: str to search in the title of the movie
    :param movies: dic of tconst: Movie
    :return: None
    """
    print('processing: CONTAINS ' + titleType + ' ' + words)
    start = time.perf_counter()
    match = False
    for m in movies:
        m = movies[m]
        if (m.titleType == titleType) and (words in m.primaryTitle):
            print('\t' + m.print())
            match = True
    if not match:
        print('\tNo match found!')
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')


def YEAR_AND_GENRE(titleType, startYear, genre, movies):
    """
    searches movies for a Movie with a specified titleType that has a matching startYear and genre and prints them out
    :param titleType: attribute of Movie dataclass
    :param startYear: attribute of Movie dataclass
    :param genre: attribute of Movie dataclass
    :param movies: dic of tconst: Movie
    :return: None
    """
    print('processing: YEAR_AND_GENRE ' + titleType + ' ' + str(startYear) + ' ' + genre)
    start = time.perf_counter()
    matches = {}
    for m in movies:
        m = movies[m]
        if (m.titleType == titleType) and (m.startYear == startYear) and (genre in m.genres):
            matches[m.tconst] = m
    if len(matches) > 0:
        for m in sorted(matches, key=lambda x: matches[x].primaryTitle):
            print('\t' + matches[m].print())
    else:
        print('\tNo match found!')
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')


def RUNTIME(titleType, startTime, endTime, movies):
    """
    searches movies for a Movie with a specified titleType that has a runtime between startTime and endTime and
        prints them out
    :param titleType: attribute of Movie dataclass
    :param startTime: lower end of runtime search range
    :param endTime: upper end of runtime search range
    :param movies: dic of tconst: Movie
    :return: None
    """
    print('processing: RUNTIME ' + titleType + ' ' + str(startTime) + ' ' + str(endTime))
    start = time.perf_counter()
    matches = {}
    for m in movies:
        m = movies[m]
        if (m.titleType == titleType) and (m.runTimeMinutes >= startTime) and (m.runTimeMinutes <= endTime):
            matches[m.tconst] = m
    if len(matches) > 0:
        for m in sorted(matches, key=lambda x: (-matches[x].runTimeMinutes, matches[x].primaryTitle)):
            print('\t' + matches[m].print())
    else:
        print('\tNo match found!')
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')


def MOST_VOTES(titleType, topNum, movies, reviews):
    """
    searches reviews and moves for a movie with a specified titleType that has the most votes and prints the
        top (topNum) of them
    :param titleType: attribute of Movie dataclass
    :param topNum: limit of Movies to print
    :param movies: dic of tconst: Movie
    :param reviews: dic of tconst: Rating
    :return: None
    """
    print('processing: MOST_VOTES ' + titleType + ' ' + str(topNum))
    start = time.perf_counter()
    matches = {}
    for m in movies:
        m = movies[m]
        if (m.titleType == titleType) and (m.tconst in reviews):
            matches[m.tconst] = m
    if len(matches) > 0:
        i = 1
        for m in sorted(matches, key=lambda x: (-int(reviews[x].numVotes), matches[x].primaryTitle)):
            if (topNum - i >= 0):
                print('\t' + str(i) + '. VOTES: ' + str(reviews[m].numVotes) + ', MOVIE: ' + matches[m].print())
                i += 1
    else:
        print('\tNo match found!')
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')

def TOP(titleType, topNum, startYear, endYear, movies, reviews):
    """
    searches reviews and moves for a movie with a specified titleType that has the largest averageRating within each
        year defined by the range from startYear to endYear and prints out the top (topNum) of them per year
    :param titleType: attribute of Movie dataclass
    :param topNum: limit of Movies to print per year
    :param startYear: lower end of year search range
    :param endYear: upper end of year search range
    :param movies: dic of tconst: Movie
    :param reviews: dic of tconst: Rating
    :return: None
    """
    print('processing: TOP ' + titleType + ' ' + str(topNum) + ' ' + str(startYear) + ' ' + str(endYear))
    start = time.perf_counter()
    matches, msort = {}, {}
    for m in movies:
        m = movies[m]
        if (m.titleType == titleType) and (m.tconst in reviews) and (m.startYear >= startYear) and (m.startYear <= endYear)  and (int(reviews[m.tconst].numVotes) >= 1000):
            matches[m.tconst] = m
    if len(matches) > 0:
        msort = sorted(matches, key=lambda x: (matches[x].startYear, -float(reviews[x].averageRating), -int(reviews[x].numVotes), matches[x].primaryTitle))
    for y in range(startYear, endYear + 1):
        print('\tYEAR: ' + str(y))
        temp = {}
        for m in msort:
            if (matches[m].startYear == y):
                temp[m] = matches[m]
        if (len(temp) <= 0):
            print('\t\tNo match found!')
        else:
            i = 1
            for m in temp:
                if (topNum - i >= 0):
                    print('\t\t' + str(i) + '. RATING: ' + str(reviews[m].averageRating) + ', VOTES: ' + str(reviews[m].numVotes) + ', MOVIE: ' + matches[m].print())
                    i += 1
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')

def main():
    """
    Searches either a large or small database of movies and their ratings based on different search queries defined in an input file
    :return: None
    """
    # how to process input queries.
    # this loop automatically terminates when EOF is reached from the file,
    # or the user enters ^D to terminate standard input

    file1, file2, size = getInputFiles()

    print('\nreading data/' + size + '.basics.tsv into dict...')
    start = time.perf_counter()
    movies = readMovies(file1)
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')

    print('reading data/' + size + '.ratings.tsv into dict...')
    start = time.perf_counter()
    ratings = readRatings(file2, movies)
    print('elapsed time (s): ' + str(time.perf_counter() - start) + '\n')

    print('Total movies: ' + str(len(movies)))
    print('Total ratings: ' + str(len(ratings)) + '\n')

    for line in sys.stdin:
        line = line.split(' ')
        line[-1] = line[-1].replace('\n', '')
        if (line[0] == 'LOOKUP'):
            LOOKUP(line[1], movies, ratings)
        if (line[0] == 'CONTAINS'):
            words = ''
            for i in range(2, len(line)):
                words = words + ' ' + line[i]
            words = words[1:]
            CONTAINS(line[1], words, movies)
        if (line[0] == 'YEAR_AND_GENRE'):
            YEAR_AND_GENRE(line[1], int(line[2]), line[3], movies)
        if (line[0] == 'RUNTIME'):
            RUNTIME(line[1], int(line[2]), int(line[3]), movies)
        if (line[0] == 'MOST_VOTES'):
            MOST_VOTES(line[1], int(line[2]), movies, ratings)
        if (line[0] == 'TOP'):
            TOP(line[1], int(line[2]), int(line[3]), int(line[4]), movies, ratings)


if __name__ == '__main__':
    main()
