from django import forms


YEAR_RANGE = tuple([(i, i) for i in range(1945,2018)])

class SentimentFinder(forms.Form):
    year = forms.ChoiceField(label="Pick a Year",
                             choices=YEAR_RANGE,
                             required=True)
