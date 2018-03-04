from django.db import models
from django.utils import timezone

import datetime
import csv
import pandas as pd
#import wiki_data as wk

EVENTS_FILENAME = '../all_events.csv'
MEDIA_FILENAME = '../temporary.csv'

class Event(models.Model):
    '''
    represents event table in sql db
    '''
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=30)
    text = models.TextField()

    def __str__(self):
        event_string = "{} {}: {}".format(self.month, self.year, self.text[:100])
        return event_string

class Media(models.Model):
    '''
    represents media table in sql db
    '''
    year = models.CharField(max_length=4)
    media_type = models.CharField(max_length=5, choices=(('book', "Book"),
                                                         ('movie', "Movie"),
                                                         ('song', "Song"),))
    detailed_text = models.TextField()
    title = models.TextField()

    def __str__(self):
        media_string = "{} ({}) - {}".format(self.title, self.year, self.media_type)
        return media_string


class Year(models.Model):
    '''
    each year has a table with events
    each year is also related to sentiments and songs/movies/books
    '''
    pass

class Sentiment(models.Model):
    # many to many year field
    pass



def construct_db():
    edf = wk.create_events_df(1945, 2018)
    years = edf['Year'].unique()

    # create year db
    for y in years:
        yrow = Year(year=y)
        yrow.save()

    for idx, row in edf.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()



def create_event_table(filename):
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()

def create_media_table(filename):
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'type', 'plot', 'title'],
                    index_col='idx')
    for idx, row in df.iterrows():
        media = Media(year=row.year, type=row.type, detailed_text=row.plot, title=row.title)
        media.save()
