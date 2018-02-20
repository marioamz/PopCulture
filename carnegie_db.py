#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 12:16:52 2018

@author: crismacgregor
"""

import numpy as np
import pandas as pd
import re
import wikipedia as wp
import jellyfish as jf



'''
BOOKS
'''
path_file_plots = "CM books/booksummaries.txt"
PATH_FILE_BOOKS = "NYTimesBestSellers.xlsx"


def get_plots(path_books,path_file_plots):
    '''
    This function gets the plots from the books.
    '''
    bsbooks_df = pd.read_excel(PATH_FILE_BOOKS)
    cmbooks_df = pd.read_csv(path_file_plots, sep='\t', header = None, index_col= None,
                           names = ["Wikipedia article ID", "Freebase ID", "Book title", 
                                  "Author", "Publication date", "Book genres", "Plot"],
                           error_bad_lines= False)
    
    cmbooks_df.rename(columns = {"Book title": "Title"}, inplace = True)
    bsbooks_df["Plot"] = ""
    exact_matches(bsbooks_df, cmbooks_df)

def exact_matches(df1, df2 ): 
    '''
    Comment: yields 734- 509 matches. 
    '''
    for i in range(0, len(bsbooks_df)):
        temp = cmbooks_df[cmbooks_df.Author == bsbooks_df.Author.loc[i]]
        for k in range(0, len(temp)):
            if bsbooks_df.Title.loc[i] == temp.Title.iloc[k]:
                bsbooks_df.Plot.loc[i] = temp.Plot.iloc[k]
                break

def non_matches_filter: 

    non_exact = bsbooks_df[bsbooks_df.Plot == ""]               
    for i in range(len(non_exact)):
        if i in non_exact.index: 
            for k in range(len(cmbooks_df)):
                if non_exact.Title.loc[i] == cmbooks_df.Title.iloc[k]:    
                    
                    s1 = str(non_exact.Author.loc[i]).replace(, '')
                    s1 = jf.match_rating_codex(str(non_exact.Author.loc[i]))

                    s2 = jf.match_rating_codex(str(cmbooks_df.Author.iloc[k]))
                    if jf.match_rating_comparison(s1, s2):
                        bsbooks_df.Plot.loc[i] = cmbooks_df.Plot.iloc[k]
                        break
                    else: 
                        continue
        
        
        
        

