from django import forms

class YearForm(forms.Form):
    year = forms.ChoiceField(label='Pick a Year! ',
                             choices=tuple([(i, i) for i in range(1945,2019)]),
                             required=True)
