#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:52:28 2018

@author: mariomoreno
"""

import wikipedia as wp
import pandas as pd

books_df = pd.read_excel("/Users/mariomoreno/Desktop/Grad School/CS 12200/PopCult/PopCulture/NYTimesBestSellers.xlsx")


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
        
    