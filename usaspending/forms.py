import datetime

from django import forms
from salesforce.SalesforceClient import SalesforceClient


def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r,r) for r in reversed(range(2008, current_year()+1))]

class USASpendingForm(forms.Form):
    year = forms.ChoiceField(choices=year_choices())
