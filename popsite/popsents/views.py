# ORIGINAL

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import SentimentFinder

import random

EMOJI_DICT = {"anticipation": "&#x1F648;",
              "anger": "&#x1F621;",
              "joy": "&#x1F606;",
              "trust": "&#x1F64F;",
              "fear": "&#x1F631;",
              "surprise": "&#x1F47B;",
              "sadness": "&#x1F62D;",
              "disgust": "&#x1F4A9;"}


def home_page(request):
    '''
    Home Page View
    Button links to Select Year View
    '''

    template = 'popsents/project_home.html'

    return render(request, template)


def find_sentiment(request):
    '''
    Search Year View
    Returns results for year when user selects year from dropdown
    '''

    if request.method == "POST":
        form = SentimentFinder(request.POST)
        input_year = form.data['year']
        template = 'popsents/sentiment_finder.html'
        context = sentfinder_context(input_year)
        return render(request, template, context)

    else:
        form = SentimentFinder()


    template = 'popsents/years.html'
    context = {'form': form}

    return render(request, template, context)


def year_detail(request, event_year):
    '''
    Archive View
    Contains all events for given year
    '''

    events_set = Event.objects.filter(year=event_year)
    template_name = 'popsents/event_archive.html'
    context = {'event_year': event_year,
               'yearly_events': events_set}

    return render(request, template_name, context)


def sentfinder_context(input_year):
    '''
    Auxiliary function building context dictionary for sentiment_finder template
    Inputs: Year
    Returns: context dictionary
    '''

    context = {}
    context['year'] = input_year
    context['table'] = emojimeter(input_year)
    context['random_events'] = random_events_generator(input_year)
    context['media'] = random_media_generator(input_year)
    context['compound'] = CompoundSents.objects.filter(year=input_year)[0]

    return context

def emojimeter(input_year):
    '''
    Auxiliary function creating Emojimeter
    Inputs: Year
    Returns: html string for emoji table
    '''
    sents = TopSents.objects.filter(year=input_year).order_by('-intensity')
    context = {}

    trows = ''
    for sent in sents:
        num_emojis = int(sent.intensity)
        emoji_html = ' '.join([EMOJI_DICT[sent.emotion]] * (num_emojis))
        trow = "<tr><th scope='row'>{}</th><td>{}</td><td>{}%</td></tr>"
        trows += trow.format(sent.emotion.capitalize(), emoji_html, num_emojis)
    table = "<table class='table table-hover'><tbody>{}</tbody></table>".format(trows)

    return table


def random_events_generator(input_year):
    '''
    Returns random sample of 3 events from all events for given year
    Input: Year
    Returns: list of 3 random events
    '''

    events_set = Event.objects.filter(year=input_year)
    random_events = random.sample(set(events_set),3)

    return random_events


def random_media_generator(input_year):
    '''
    Returns random sample of 1 book, 1 movie, and 1 song for given year
    Inputs: Year
    Returns: list of strings representing media in year
    '''

    random_media = []
    for m in ('Book', 'Movie', 'Song'):
        media_set = Media.objects.filter(year=input_year, media_type=m)
        if len(media_set) > 0:
            medium = random.sample(set(media_set),1)[0]
            if m == "Movie":
                mstring = "We packed the theaters for {}.".format(medium.title)
            if m == "Song":
                mstring = "We rocked out to {} by {}.".format(medium.title.title(),
                                                              medium.author.title())
            if m == "Book":
                mstring = "We read {} by {}.".format(medium.title, medium.author)
            random_media.append(mstring)

    return random_media
