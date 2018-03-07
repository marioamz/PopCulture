from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from random import randint

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
        events_set = random_events_generator(y)
        media_set = random_media_generator(y)
        compound = CompoundSents.objects.filter(year=y)[0]
        context['events'] = events_set
        context['media'] = media_set
        context['compound'] = compound

        return render(request, template, context)
    else:
        form = SentimentFinder()
    return render(request, 'popsents/years.html', {'form': form})


def emojis(input_year):
    sents = TopSents.objects.filter(year=input_year)
    context = {}
    trows = ""
    for i, sent in enumerate(sents):
        num_emojis = int(sent.intensity // 10)
        emoji_html = ' '.join([EMOJI_DICT[sent.emotion]] * (num_emojis + 1))
        trows += "<tr><th scope='row'>{}</th><td>{}</td><td>{}%</td></tr>".format(sent.emotion, emoji_html, int(sent.intensity))
    table = "<table class='table table-hover'><tbody>{}</tbody></table>".format(trows)
    context['table'] = table
    context['year'] = input_year
    return context


def random_events_generator(input_year):
    events_set = Event.objects.filter(year=input_year)
    random_events = []
    for _ in range(3):
        random_index = randint(0, len(events_set))
        random_events.append(events_set[random_index])

    return random_events


def random_media_generator(input_year):
    media = ('Book', 'Movie', 'Song')
    random_media = []
    for m in media:
        media_set = Media.objects.filter(year=input_year, media_type=m)
        print(media_set)
        random_index = randint(0, len(media_set))
        medium = media_set[random_index]
        if m == "Book":
            mstring = "We read {} by {}".format(medium.title, medium.author)
        if m == "Movie":
            mstring = "We packed the theaters for {}".format(medium.title)
        if m == "Song":
            mstring = "We rocked out to {} by {}".format(medium.title, medium.author)
        random_media.append(mstring)
    return random_media

# currently not using
def select_year_and_type(request):
    '''
    Basic view where user selects year
    Returns a result from the database
    '''
    if request.method == "POST":
        print(request)
        form = YearForm(request.POST)
        year = form.data['year']
        mt = form.data['media_type']
        print(form)
        return year_media_detail(request, year, mt)
    else:
        form = YearForm()

    return render(request, 'popsents/years.html', {'form': form})


def year_media_detail(request, input_year, input_type):
    '''
    '''
    media_set = Media.objects.filter(year=input_year, media_type=input_type) # queryset
    print(media_set)
    template_name = 'popsents/year_media.html'
    context = {'input_year': input_year,
               'media_type': input_type,
               'media_set': media_set}
    return render(request, template_name, context)


def years_list(request):
    '''
    Index of all years covered in project
    '''
    template_name = 'popsents/year_list.html'
    years = (i for i in range(1945, 2019))
    context = {'years': years}
    return render(request, template_name, context)


def year_detail(request, event_year):
    '''
    '''
    events_set = Event.objects.filter(year=event_year) # queryset
    template_name = 'popsents/year_detail.html'
    context = {'event_year': event_year,
               'yearly_events': events_set}
    return render(request, template_name, context)


# Very basic index view

class IndexView(generic.ListView):
    '''
    '''
    template_name = 'popsents/index.html'
    context_object_name = 'random_events'

    def get_queryset(self):
        return Event.objects.order_by('id')[:100]
        #return self.get_events_by_year()

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'popsents/detail.html', {'event': event})
