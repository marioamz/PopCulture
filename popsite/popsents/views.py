from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Event, Media
from .forms import YearForm


def home_page(request):
    '''
    Home Page View
    Button links to Select Year and Type View
    '''
    template = 'popsents/home.html'
    return render(request, template)


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
