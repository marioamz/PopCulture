# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import re
import wikipedia as wp

path_file_songs = "/Users/crismacgregor/Desktop/UChi/Classes/CompSci/CS122/Project/PopCulture/billboard_lyrics_1964-2015.csv"
path_file_movie = "/Users/crismacgregor/Desktop/UChi/Classes/CompSci/CS122/Project/PopCulture/the-movies-dataset/movies_metadata.csv"
path_file_books = "/Users/crismacgregor/Desktop/UChi/Classes/CompSci/CS122/Project/PopCulture/NYTimesBestSellers.xlsx"

'''
BOOKS
'''
books_df = pd.read_excel(path_file_books)

def get_years():
    '''
    This function creates a list of years
    that we're interested in.
    '''
    year_list = [1958]
    for year in year_list:
        year_list.append(year + 1)
        if year == 2017:
            return year_list

def parsing():
    '''
    This function parses through our main Wikipedia page,
    finds the relevant links to follow
    '''
    BestSellers = wp.page("Lists of The New York Times Fiction Best Sellers")

    lists_links = BestSellers.links
    pages = []

    for link in lists_links:
        for year in get_years():
            if str(year) in lists_links:
                pages.append(link)

    return pages

def get_books():
    '''
    This function compares titles of our books in the dataframe to titles 
    that have links in the pages of bestsellers
    '''
    # do contain search
    
    books_to_parse = []
    books = []
    books_2 = []
    parsed_pages = parsing()
    
    for page in parsed_pages:
        top = wp.page(page)
        books_to_parse.append(top)
    
    for pg in books_to_parse:
        for book in pg:
            book = pg.links
            books.append(book)
            
    for book in books:
        for b in book:
            if b in books_df["Title"]:
                books_2.append(b)
        
    return books_2

def get_plots():
    '''
    This function gets the plots from the books.
    '''
    
    plots = []
    
    for book in get_books():
        book_page = wp.page(book)
        if "novel" in book_page.summary:
            plot = book_page.section("Plot")
            plots.append(plot)
        else:
            book_page = wp.page(book + "(Novel)")
            plot = book_page.section("Plot")
            plots.append(plot)
            
    return plots

#Rename to match: plot; title; year; author
'''
SONGS
'''
def songs_movie(path_file_movie):

    #Rename to match: plot; title; year; author
    songs_df = pd.read_csv(path_file_songs, sep=',', header = "infer", 
                           error_bad_lines= False, encoding="cp775")
    
    songs_df.rename(columns = {'Lyrics':'Plot', 'Song': 'Title'}, inplace = True)
    songs_df['Type'] = "Song"
    songs_df = songs_df.loc[:, ["Year","Type","Plot","Title"]]
    return songs_df

'''
MOVIES
'''

def clean_movie(path_file_movie):
    movies_df = pd.read_csv(path_file_movie, sep=',', header = "infer")
    
    movies_df.rename(columns = {'title':'Title'}, inplace = True)
    
    #Making new column exctracting Year from release_date string
    movies_df['Year'] = movies_df.release_date.str.extract(r'(\d{4})', expand=True)
    #movies_df['year'] = int(movies_df['year'])
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
    inputs: list with data frames 
    outputs: concatenated dataframe
    '''
    result = pd.concat(dfs_ls)
    
    return result




















