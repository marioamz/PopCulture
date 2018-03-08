from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

import random

from .models import Event, Media, TopSents, CompoundSents
from .forms import YearForm, SentimentFinder


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
    Button links to Select Year and Type View
    '''
    template = 'popsents/project.html'
    return render(request, template)


def find_sentiment(request):
    if request.method == "POST":
        form = SentimentFinder(request.POST)
        y = form.data['year']
        template = 'popsents/sentiment_finder.html'

        context = emojis(y)
        random_events = random_events_generator(y)
        media_set = random_media_generator(y)
        compound = CompoundSents.objects.filter(year=y)[0]
        context['random_events'] = random_events
        context['media'] = media_set
        context['compound'] = compound

        return render(request, template, context)
    else:
        form = SentimentFinder()
    return render(request, 'popsents/years.html', {'form': form})


def emojis(input_year):
    sents = TopSents.objects.filter(year=input_year).order_by('-intensity')
    context = {}
    trows = ""
    for i, sent in enumerate(sents):
        num_emojis = int(sent.intensity // 10)
        emoji_html = ' '.join([EMOJI_DICT[sent.emotion]] * (num_emojis*2 + 1))
        trows += "<tr><th scope='row'>{}</th><td>{}</td><td>{}%</td></tr>".format(sent.emotion.capitalize(), emoji_html, int(sent.intensity))
    table = "<table class='table table-hover'><tbody>{}</tbody></table>".format(trows)
    context['table'] = table
    context['year'] = input_year
    return context


def random_events_generator(input_year):
    events_set = Event.objects.filter(year=input_year)
    random_events = random.sample(set(events_set),3)
    return random_events


def random_media_generator(input_year):
    media = ('Book', 'Movie', 'Song')
    random_media = []
    for m in media:
        media_set = Media.objects.filter(year=input_year, media_type=m)
        if len(media_set) > 0:
            medium = random.sample(set(media_set),1)[0]
            if m == "Movie":
                mstring = "We packed the theaters for {}.".format(medium.title)
            if m == "Song":
                mstring = "We rocked out to {} by {}.".format(medium.title.title(), medium.author.title())
            if m == "Book":
                mstring = "We read {} by {}.".format(medium.title, medium.author)
            random_media.append(mstring)
    return random_media


def year_detail(request, event_year):
    '''
    '''
    events_set = Event.objects.filter(year=event_year)
    template_name = 'popsents/year_detail.html'
    context = {'event_year': event_year,
               'yearly_events': events_set}
    return render(request, template_name, context)
