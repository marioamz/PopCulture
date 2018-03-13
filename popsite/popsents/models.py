# ORIGINAL

from django.db import models
from django.utils import timezone

import pandas as pd

class Event(models.Model):
    '''
    Represents Event table in SQLite3 db
    '''
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=30)
    text = models.TextField(default='')

    def __str__(self):
        event_string = "{} {}: {}".format(self.month, self.year, self.text[:100])
        return event_string


class Media(models.Model):
    '''
    Represents Media table in SQLite3 db
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
    Represents Bag of Word Sentiments table in SQLite3 db
    '''
    year = models.CharField(max_length=4)
    emotion = models.CharField(max_length=20)
    intensity = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        sent_string = "{} percent of pop culture in {} exhibited {}."
        sent_string = sent_string.format(self.intensity, self.year, self.emotion)
        return sent_string

class CompoundSents(models.Model):
    '''
    Represents Vader Compoud Sentiment Score table in SQLite3 db
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


##############################
#       SQL DATA DUMP        #
##############################


EVENTS_FILENAME = '../final_events.csv'
MEDIA_FILENAME = '../final_media_df.csv'
RESULTS_FILENAME = '../emotions.csv'

def construct_db():
    '''
    Wipes out DB, Creates and Saves New Data Points
    '''

    Media.objects.all().delete()
    Event.objects.all().delete()
    TopSents.objects.all().delete()
    CompoundSents.objects.all().delete()

    create_event_table(EVENTS_FILENAME)
    create_media_table(MEDIA_FILENAME)
    create_sentiment_tables(RESULTS_FILENAME)


def create_event_table(filename):
    '''
    Creates and Saves Event Objects in DB
    '''

    df = pd.read_csv(filename, header=0,
                    names=['idx', 'year', 'month', 'event'],
                    index_col='idx')

    for idx, row in df.iterrows():
        event = Event(year=row.year, month=row.month, text=row.event)
        event.save()


def create_media_table(filename):
    '''
    Creates and Saves Media Objects in DB
    '''

    df = pd.read_csv(filename, header=0)
    df.Year = df.Year.apply(int)
    for i, row in df.iterrows():
        media = Media(year=row.Year, media_type=row.Type, title=row.Title, author=row.Author)
        media.save()


def create_sentiment_tables(filename):
    '''
    Creates and Saves TopSents, CompSents Objects in DB
    '''

    df = pd.read_csv(filename)
    df.Year = df.Year.apply(int)
    FEELS = ["anticipation", "anger", "joy", "trust", "fear",
             "surprise", "sadness", "disgust"]

    for i, row in df.iterrows():
        for f in FEELS:
            intense = "{} percentage".format(f)
            sent = TopSents(year=int(row.Year), emotion=f, intensity=row[intense])
            sent.save()
        c = CompoundSents(year=int(row.Year), compound=row['compound'],
                          positive=row.pos, neutral=row.neu, negative=row.neg)
        c.save()
