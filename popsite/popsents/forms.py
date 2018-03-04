from django import forms
from .models import Event, Media


class YearForm(forms.Form):
    year = forms.CharField(label='Year', max_length=4)
