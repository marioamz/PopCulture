from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the landing page for Pop Culture Renegades.")
# Create your views here.
