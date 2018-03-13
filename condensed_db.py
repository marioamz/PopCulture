#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import jellyfish as jf


'''
BOOKS
'''
PATH_FILE_SONGS = "billboard_lyrics_1964-2015.csv"
PATH_FILE_MOVIES = "movies_metadata.csv"
PATH_FILE_BOOKS = "NYTimesBestSellers.xlsx"
PATH_FILE_PLOTS = "CM books/booksummaries_nc.txt"


def clean_books(path_file_b, path_file_p):
    '''
    This function takes two CSV files with plots for books and bestselling
    books, calls two functions to merge them on Title and then similar Titles
    and Authors, and returns a dataframe with relevant columns for books.
    '''

    bsbooks_df = pd.read_excel(path_file_b)
    cmbooks_df = pd.read_csv(path_file_p, sep='\t', index_col= 2,  \
                             names = ["Wikipedia article ID", "Freebase ID",\
                                      "Book title","Author", "Publication date",\
                                      "Book genres", "Plot"], encoding="utf_8", \
                                      error_bad_lines=True)

    cmbooks_df.rename(columns = {"Publication date": "Year"}, inplace = True)

    #To get same format for book year
    cmbooks_df['Year'] = cmbooks_df.Year.str.extract(r'(\d{4})', expand=True)

    #Update plots by exact title match
    clean_books_build(bsbooks_df, cmbooks_df)

    #Update plots by author match and similar titles
    clean_books_2ndstage(bsbooks_df, cmbooks_df)

    bsbooks_df['Type'] = "Book"
    bsbooks_df = bsbooks_df.loc[:, ["Year","Type","Plot","Title", "Author"]]

    return bsbooks_df

def clean_books_build(df1, df2):
    '''
    Updates plots for those with exact titles in two dataframes.
    '''

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
    checking that they are from the same author. This is to find plots for
    those who did not match by exact title.
    '''

    non_exact = df1[df1.Plot.isnull()]

    for i in range(len(non_exact)):
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

    songs_df = pd.read_csv(path_file, header = "infer",
                           error_bad_lines= False, encoding="cp775")

    songs_df.rename(columns = {'Lyrics':'Plot', 'Song': 'Title', 'Artist':'Author'}, inplace = True)
    songs_df['Type'] = "Song"
    songs_df = songs_df.loc[:, ["Year", "Type", "Plot", "Title", "Author"]]

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

    movies_df = pd.read_csv(path_file, header = "infer")
    movies_df.rename(columns = {'title':'Title',
                                'overview': 'Plot',
                                'production_companies': 'Author'}, inplace=True)

    #Making new column exctracting Year from release_date string
    movies_df['Year'] = movies_df.release_date.str.extract(r'(\d{4})', expand=True)

    #Deleting non-released movies, previous to 1940s ad NaN
    movies_df = movies_df.dropna(subset=['Year'])
    movies_df.Year = movies_df.Year.astype(int)
    movies_df = movies_df[(movies_df.Year < 2018) & (movies_df.Year > 1940)]

    # Use Popularity, Drop outliers, Keep Top 100
    movies_df.popularity = movies_df.popularity.astype(float)
    movies_df = movies_df.where(movies_df.popularity != 0.0)
    outliers = movies_df.popularity.quantile(.95)
    movies_df = movies_df.where(movies_df.popularity <= outliers)
    movies_df = movies_df.dropna(subset=['popularity'])
    movies_df = movies_df.sort_values('popularity', ascending=False).groupby('Year').head(100)

    movies_df['Type'] = "Movie"
    movies_df = movies_df.loc[:, ["Year", "Type", "Plot", "Title", "Author"]]

    return movies_df


def create_file():
    '''
    Concatenates dataframes for each media type and returns final df
    Inputs: None
    Returns:
        CSV file
        Final df
    '''

    songs_df = clean_songs(PATH_FILE_SONGS)
    movies_df = clean_movies(PATH_FILE_MOVIES)
    books_df = clean_books(PATH_FILE_BOOKS, PATH_FILE_PLOTS)
    result = pd.concat([songs_df, movies_df, books_df])
    result.to_csv("final_media_df.csv")
    result.reset_index(inplace=True)

    return result
