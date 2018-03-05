from django import forms
from .models import Media

class YearForm(forms.Form):
    year = forms.ChoiceField(label='Pick a Year! ',
                             choices=tuple([(i, i) for i in range(1945,2019)]),
                             required=True)

    media_type = forms.ChoiceField(label="and medium of choice",
                                   choices=(('Book', "Book"),
                                            ('Movie', "Movie"),
                                            ('Song', "Song")))
