from django.db import models
from django.utils import timezone

import datetime
import csv
import pandas as pd

EVENTS_FILENAME = '../all_events.csv'
MEDIA_FILENAME = '../final_media_df_UPDT.csv'
SENTS_FILENAME = '../test.csv'

class Event(models.Model):
    '''
    represents event table in sql db
    '''
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=30)
    text = models.TextField(default='')

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
    title = models.TextField(default='')
    author = models.TextField(default='')

    def __str__(self):
        media_string = "{} ({}) - {}".format(self.title, self.year, self.media_type)
        return media_string

class TopSents(models.Model):
    '''
    '''
    year = models.CharField(max_length=4)
    emotion = models.CharField(max_length=20)
    rank = models.IntegerField()
    intensity = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        sent_string = "Top {} emotion for {} was {}, with an intensity of {}.".format(
                        self.rank, self.year, self.emotion, self.intensity)
        return sent_string

class CompoundSents(models.Model):
    '''
    '''
    year = models.CharField(max_length=4)
    compound = models.DecimalField(max_digits=8, decimal_places=3)
    positive = models.DecimalField(max_digits=8, decimal_places=3)
    neutral = models.DecimalField(max_digits=8, decimal_places=3)
    negative = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        comp_string = ''
        if self.compound > 0:
            comp_string = 'positive'
        elif self.compound < 0:
            comp_string = 'negative'
        else:
            comp_string = 'neutral'
        return "{} was filled with {} vibes.".format(self.year, comp_string)

########################
#  DATA DUMP INTO SQL  #
########################

def construct_db():
    '''
    '''
    Media.objects.all().delete()
    Event.objects.all().delete()

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
    df = pd.read_csv(filename, header=0)
    df.Year = df.Year.apply(int)
    for i, row in df.iterrows():
        print(row.Year)
        media = Media(year=row.Year, media_type=row.Type, title=row.Title, author=row.Author)
        #print(media.year)
        media.save()


def create_sentiment_tables(filename):
    df = pd.read_csv(filename, header=None,
                     names = ['year', 'emo1', 'freq1', 'emo2', 'freq2',
                              'emo3', 'freq3',
                              'compound', 'positive', 'neutral', 'negative'])
    for i, row in df.iterrows():
        print(row['year'])
        t1 = TopSents(year=row['year'], emotion=row.emo1, rank=1, intensity=row.freq1)
        t2 = TopSents(year=row['year'], emotion=row.emo2, rank=2, intensity=row.freq2)
        t3 = TopSents(year=row['year'], emotion=row.emo3, rank=3, intensity=row.freq3)
        c = CompoundSents(year=row['year'], compound=row['compound'], positive=row['positive'],
                      neutral=row['neutral'], negative=row['negative'])
        t1.save()
        t2.save()
        t3.save()
        c.save()
