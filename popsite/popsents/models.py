from django.db import models
from django.utils import timezone

import datetime
import csv
import pandas as pd

EVENTS_FILENAME = '../../events.csv'
MEDIA_FILENAME = '../../temporary.csv'

class Event(models.Model):
    '''
    represents event table in sql db
    '''
    year = models.IntegerField(max_length=4)
    month = models.CharField(max_length=12)
    text = models.TextField()

    def __str__(self):
        event_string = "{} {}: {}".format(self.month, self.year, self.text[:100])
        return event_string

class Media(models.Model):
    '''
    represents media table in sql db
    '''
    year = models.IntegerField()
    MTYPE = (
        ('Book', 'Book'),
        ('Song', 'Song'),
        ('Movie', 'Movie'),
    )
    media_type = models.CharField(max_length=5, choices=MTYPE)
    detailed_text = models.TextField()
    title = models.TextField()

    def __str__(self):
        media_string = "{} ({}) - {}".format(self.title, self.year, self.media_type)
        return media_string
'''
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

'''


def create_event_table(filename):
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(row.year, row.month, row.event)
        event.save()

def create_media_table(filename):
    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'type', 'plot', 'title'],
                    index_col='idx')
    for idx, row in df.iterrows():
        media = Media(row.year, row.type, row.plot, row.title)
        media.save()
