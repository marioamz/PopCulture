# ORIGINAL

from django.urls import path
from . import views

app_name = 'popsents'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('years/', views.find_sentiment, name='years'),
    path('years/<int:event_year>', views.year_detail, name='year_detail'),
]
