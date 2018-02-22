# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import re
import wikipedia as wp

PATH_FILE_SONGS = "billboard_lyrics_1964-2015.csv"
PATH_FILE_MOVIES = "movies_metadata.csv"
PATH_FILE_BOOKS = "NYTimesBestSellers.xlsx"
PATH_FILE_PLOTS = "CM books/booksummaries.txt"

songs_df = clean_songs(PATH_FILE_SONGS)
movies_df = clean_movies(PATH_FILE_MOVIES)
books_df = clean_books(PATH_FILE_BOOKS, PATH_FILE_PLOTS)
concatenate([songs_df, movies_df, books_df])

'''
BOOKS
'''

def clean_books(path_file_b, path_file_p):
    '''
    This function gets the plots from the books.
    '''
    bsbooks_df = pd.read_excel(path_file_b)
    cmbooks_df = pd.read_csv(path_file_p, sep='\t', header = None, index_col= None,
                           names = ["Wikipedia article ID", "Freebase ID", "Book title",
                                  "Author", "Publication date", "Book genres", "Plot"],
                           error_bad_lines= False)

    cmbooks_df.rename(columns = {"Book title": "Title"}, inplace = True)
    cmbooks_df.rename(columns = {"Publication date": "Year"}, inplace = True)

    exact_matches(bsbooks_df, cmbooks_df)

def clean_books_build(df1, df2):
    '''
    Matching directly on title: 322 matches
    '''
    # this builds a list of all the titles of bestsellers
    title_list = []
    for title in df1.Title:
        title_list.append(title)

    # this creates a matching dataframe
    temp_df = pd.DataFrame(df2['Title'].isin(title_list))
    matching = temp_df[temp_df.Title != False]

    # filters cm books to just the matches, deduplicates, drops irrelevant cols
    cmbooks = df2.loc[list(matching.index)].drop_duplicates(subset = "Title")
    cmbooks.drop(["Author", "Year", "Book genres", "Wikipedia article ID", "Freebase ID", axis = 1, inplace=True])

    # final dataframe
    books = pd.merge(df1, cmbooks, on = "Title")

    return books


'''
SONGS
'''

def clean_songs(path_file):
    '''
    Loads songs data into pandas dataframe

    Inputs: filename
    Returns:
        pandas df of songs data
    '''

    #Rename to match: plot; title; year; author
    songs_df = pd.read_csv(path_file, sep=',', header = "infer",
                           error_bad_lines= False, encoding="cp775")

    songs_df.rename(columns = {'Lyrics':'Plot', 'Song': 'Title'}, inplace = True)
    songs_df['Type'] = "Song"
    songs_df = songs_df.loc[:, ["Year","Type","Plot","Title"]]
    return songs_df

'''
MOVIES
'''

def clean_movies(path_file):
    '''
    Loads movies data in pandas dataframe
    Inputs: filename
    Returns
        pandas df of movies data
    '''

    movies_df = pd.read_csv(path_file, sep=',', header = "infer")
    movies_df.rename(columns = {'title':'Title'}, inplace = True)

    #Making new column exctracting Year from release_date string
    movies_df['Year'] = movies_df.release_date.str.extract(r'(\d{4})', expand=True)
    movies_df["Year"].value_counts()

    #Deleting non-released movies, previous to 1940s ad NaN
    movies_df = movies_df.dropna(subset=["Year"])
    movies_df.Year = movies_df.Year.astype(int)
    movies_df = movies_df[(movies_df.Year<2018)]
    movies_df = movies_df[(movies_df.Year>1940)]
    movies_df["Year"].value_counts()
    movies_df = movies_df.dropna(subset=["Year"])

    #By year get top 50 according to revenues
    #movies_df.where(movies_df.revenue==0).count()
    #movies_df = movies_df.where(movies_df.revenue!=0)
    #·Gives us info on nan or 0.
    #Problem = we have approximately 35,000 out of 45000 movies without info on revenues

    '''
    Using popularity score instead of revenue: Problem - we have outliers up to547 but
    the mean is 3 so there must be some inconsistency in the data and data sources
    do not cite meaning of popularity or its computation. To use as a referent, we
    trim right hand outliers p(95) and work with the remaining.
    '''

    movies_df.popularity = movies_df.popularity.astype(float)
    movies_df = movies_df.where(movies_df.popularity != 0.0)
    x = movies_df.popularity.quantile(.95)
    movies_df = movies_df.where(movies_df.popularity <= x)
    movies_df = movies_df.dropna(subset=["popularity"])

    movies_df['Type'] = "Movie"
    movies_df.rename(columns = {"overview":"Plot"}, inplace = True)

    movies_df = movies_df.sort_values('popularity',ascending = False).groupby('Year').head(100)
    movies_df = movies_df.loc[:, ["Year","Type","Plot","Title"]]

    return movies_df

#Concatenate

def concatenate(dfs_ls):
    '''
    Inputs: list of pandas df for each type of media
    Returns: final df
    '''
    result = pd.concat(dfs_ls)

    return result
