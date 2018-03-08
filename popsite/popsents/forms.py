from django import forms
from .models import Media


YEAR_RANGE = tuple([(i, i) for i in range(1945,2018)])

class YearForm(forms.Form):
    year = forms.ChoiceField(label='Pick a Year! ',
                             choices=YEAR_RANGE,
                             required=True)

    media_type = forms.ChoiceField(label="and medium of choice",
                                   choices=(('Book', "Book"),
                                            ('Movie', "Movie"),
                                            ('Song', "Song")))

class SentimentFinder(forms.Form):
    year = forms.ChoiceField(label="Pick a Year",
                             choices=YEAR_RANGE,
                             required=True)
