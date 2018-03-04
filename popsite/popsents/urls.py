from django.urls import path

from . import views

app_name = 'popsents'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:event_id>/', views.detail, name='detail'),
    path('years/', views.select_year, name='years'),
    path('year_list/<int:event_year>', views.year_detail, name='year_detail'),
    path('year_list/', views.years_list, name='year_list'),
]
'''
path function is passed 4 arguments
2 required: route and views
    - route: 'string' that contains url pattern
    - view: calls specified view function with httprequest obj
2 optional: kwargs and name
    - kwargs
    - name: naming it lets you refer to url unambiguously

'''
