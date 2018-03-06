import csv
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# read in final dataframes
os.chdir('/Users/mariomoreno/Desktop/Grad School/CS 12200/PopCult/PopCulture')
cluster = pd.read_csv('model_clust_attempt.csv')
bagowords = pd.read_csv('model_wordcounts.csv')

# set appropriate colors for emotions
ant = 'c'
ang = 'r'
joy = 'y'
trust = 'm'
fear = 'k'
surprise = 'w'
sadness = 'b'
disgust = 'g'

def cluster_plot(model_df):
    '''
    This function takes in a dataframe, creates
    matrices for the x-axis(year) and for each feeling for the
    y-axis. It superimposes the plots on each other to create a
    final graph.
    '''
    # creates x axis
    x_axis = model_df['Year'].as_matrix()

    # creates all the y axis
    y_axis_ant = model_df['anticipation percentage'].as_matrix()
    y_axis_ang = model_df['anger percentage'].as_matrix()
    y_axis_joy = model_df['joy percentage'].as_matrix()
    y_axis_trust = model_df['trust percentage'].as_matrix()
    y_axis_fear = model_df['fear percentage'].as_matrix()
    y_axis_surprise = model_df['surprise percentage'].as_matrix()
    y_axis_sadness = model_df['sadness percentage'].as_matrix()
    y_axis_disgust = model_df['disgust percentage'].as_matrix()

    # builds the plot
    plt.scatter(x_axis, y_axis_ant, color = ant)
    plt.scatter(x_axis, y_axis_ang, color = ang)
    plt.scatter(x_axis, y_axis_joy, color = joy)
    plt.scatter(x_axis, y_axis_trust, color = trust)
    plt.scatter(x_axis, y_axis_fear, color = fear)
    plt.scatter(x_axis, y_axis_surprise, color = surprise)
    plt.scatter(x_axis, y_axis_sadness, color = sadness)
    plt.scatter(x_axis, y_axis_disgust, color = disgust)

    #plots it
    plt.show()
