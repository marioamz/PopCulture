#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import re
import wikipedia as wp
import jellyfish as jf

'''
BOOKS
'''
PATH_FILE_SONGS = "billboard_lyrics_1964-2015.csv"
PATH_FILE_MOVIES = "movies_metadata.csv"
PATH_FILE_BOOKS = "NYTimesBestSellers.xlsx"
PATH_FILE_PLOTS = "CM books/booksummaries_nc.txt" #Non corrupted file


def clean_books(path_file_b, path_file_p):
    '''
    This function returns a dataframe with plots for the books in a list of
    bestselling books from the New York times, using a csv file that contains
    plots for a large amount of books.
    '''
    bsbooks_df = pd.read_excel(path_file_b)
    cmbooks_df = pd.read_csv(path_file_p, sep='\t', index_col= 2,  names = ["Wikipedia article ID", "Freebase ID", "Book title","Author", "Publication date", "Book genres", "Plot"], encoding="utf_8", error_bad_lines=True)
    cmbooks_df.rename(columns = {"Book title": "Title"}, inplace = True)
    cmbooks_df.rename(columns = {"Publication date": "Year"}, inplace = True)

    #To get same format for book year
    cmbooks_df['Year'] = cmbooks_df.Year.str.extract(r'(\d{4})', expand=True)
    cmbooks_df.index = cmbooks_df.index.str.title()
    bsbooks_df.Title = bsbooks_df.Title.str.title()

    #Pt 1 of updating plots
    clean_books_build(bsbooks_df, cmbooks_df)
    # #Pt 2 of updating plots
    clean_books_2ndstage(bsbooks_df, cmbooks_df)
    #
    # return bsbooks_df
    return bsbooks_df

def clean_books_build(df1, df2):
    '''
    Updates plots for those with exact titles in two dataframes.
    '''
    # this builds a list of all the titles of bestsellers
    df1.loc[:, "Plot"] = None

    title_list = []
    only_titles = []

    for inx, row in df1.iterrows():
        only_titles.append(row.Title)
        title_list.append((inx, row.Title))

    cmbooks = df2.loc[only_titles]
    for book in title_list:
        if (type(book[1]) is str) and (type(cmbooks.loc[book[1]].Plot) is str):
                df1.loc[book[0], "Plot"] = cmbooks.loc[book[1]].Plot


def clean_books_2ndstage(df1, df2):
    '''
    Updates plots for match titles that are similar (although not exact),
    checking that they are from the same author. This is to find plots for those
    who did not match by crossing exact title.
    '''

    #To make more exact, we can block on Author´s first name.

    non_exact = df1[df1.Plot.isnull()]
    count = 0
    for i in range(len(non_exact)):
        #Blocking on author
        temp = df2[(df2["Author"] == non_exact.iloc[i].Author)]
        for k in temp.iterrows():
            s1_ = str(non_exact.iloc[i].Title)
            s2_ = str(k[0])
            s1_upd = s1_.encode('ascii', 'ignore').decode('ascii')
            s2_upd = s2_.encode('ascii', 'ignore').decode('ascii')
            s1 = jf.match_rating_codex(s1_upd)
            s2 = jf.match_rating_codex(s2_upd)
            if (jf.match_rating_comparison(s1, s2)):
                df1.Plot.loc[i] = k[1].Plot
                count += 1
                break

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
    #Problem = we have approximately 35,000 out of 45000 movies without info on
    #revenues

    '''
    Using popularity score instead of revenue: Problem - we have outliers up
    to547 but the mean is 3 so there must be some inconsistency in the data and
    data sources do not cite meaning of popularity or its computation. To use as
    a referent, we trim right hand outliers p(95) and work with the remaining.
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

def concatenate(dfs_ls):
    '''
    Inputs: list of pandas df for each type of media
    Returns: final df
    '''
    result = pd.concat(dfs_ls)

    return result


def create_file():

    songs_df = clean_songs(PATH_FILE_SONGS)
    movies_df = clean_movies(PATH_FILE_MOVIES)
    books_df = clean_books(PATH_FILE_BOOKS, PATH_FILE_PLOTS)
    result = concatenate([songs_df, movies_df, books_df])

    return result
