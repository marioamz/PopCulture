from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Event, Media
from .forms import YearForm

# I want to create a form to select a year and
# have it return a queryset from the database using that year

def select_year(request):
    form = YearForm()
    return render(request, 'popsents/years.html', {'form': form})

def get_events_by_year(request):
    yr = request.GET['input_year']
    events_set = Event.objects.filter(year=yr) # queryset
    template_name = 'popsents/year_detail.html'
    context = {'event_year':  yr,
               'yearly_events': events_set}
    return render(request, template_name, context)

# That was not working so I was trying to have a list of all years
# and to have a link to a page that returns all events for that given year

def years_list(request):
    template_name = 'popsents/year_list.html'
    q = set([event.year for event in Event.objects.all()])
    context = {'years': q}
    return render(request, template_name, context)

def year_detail(request, event_year):
    events_set = Event.objects.filter(year=event_year) # queryset
    template_name = 'popsents/year_detail.html'
    context = {'event_year': event_year,
               'yearly_events': events_set}
    return render(request, template_name, context)

# Very basic index view

class IndexView(generic.ListView):
    template_name = 'popsents/index.html'
    context_object_name = 'random_events'

    def get_queryset(self):
        return Event.objects.order_by('id')[:100]
        #return self.get_events_by_year()


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'popsents/detail.html', {'event': event})
