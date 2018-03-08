from django.db import models
from django.utils import timezone

import datetime
import csv
import pandas as pd


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
    intensity = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        sent_string = "{} percent of pop culture in {} exhibited {}.".format(self.intensity, self.year, self.emotion)
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
