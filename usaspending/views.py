from django.shortcuts import render
from django.http import HttpResponse
from subprocess import Popen

from django.views.generic import TemplateView, FormView
from usaspending.forms import USASpendingForm
from usaspending.USASpending import USASpendingReporter

class USASpendingView(FormView):
    template_name = 'spending.html'
    success_url = 'success'
    form_class = USASpendingForm

    def form_valid(self, form):
        year =  form.cleaned_data.get('year')
        reporter = USASpendingReporter()
        reporter.find_spending_for_all_clients(int(year))
        return super(USASpendingView, self).form_valid(form)
