from django.db import models
from django.utils import timezone

import datetime
import csv
import pandas as pd
#import wiki_data as wk

EVENTS_FILENAME = '../all_events.csv'
MEDIA_FILENAME = '../../temporary.csv'

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


class Sentiment(models.Model):
    # many to many year field
    pass

########################
#  DATA DUMP INTO SQL  #
########################

def construct_db():

    create_event_table(EVENTS_FILENAME)
    create_media_table(MEDIA_FILENAME)

def create_event_table(filename):
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()

def create_media_table(filename):
    with open(filename) as media_db:
        reader = csv.reader(media_db)
        for row in (r for i, r in enumerate(reader) if i>0):
            media = Media(year=row[1], media_type=row[2],
                          detailed_text=row[3], title=row[4])
            media.save()
