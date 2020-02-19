import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.core.management import call_command
from usaspending.USASpending import USASpendingReporter
from accounts.models import Account
from salesforce.SalesforceClient import SalesforceClient

class USASpendingView(TemplateView):
    template_name = 'spending.html'
    success_url = 'success'

    def form_valid(self, form):
        year =  form.cleaned_data.get('year')
        reporter = USASpendingReporter()
        reporter.find_spending_for_all_clients(int(year))
        return super(USASpendingView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(USASpendingView, self).get_context_data(**kwargs)
        context['running'] = Account.objects.filter(usa_spending_updated=True).count()
        context['all'] = Account.objects.count()
        context['finished'] = (context['running'] == context['all'])
        context['last_run'] = open(settings.BASE_DIR + '/usaspending.txt', 'r').read()
        today = datetime.datetime.now().strftime("%D")
        recently_run = (context['last_run'] == today)
        context['session'] = recently_run or (not context["finished"] and context['last_run'])
        return context

    def post(self, request, *args, **kwargs):
        last_run = open(settings.BASE_DIR + '/usaspending.txt', 'r').read().strip()

        if last_run:
            last_run = datetime.datetime.strptime(last_run, '%m/%d/%y')
            today = datetime.datetime.now()
            datediff = (today - last_run).days
            if datediff > 20:
                call_command("import_salesforce")

        f = open(settings.BASE_DIR + '/usaspending.txt', 'w+')
        f.write(datetime.datetime.now().strftime("%D"))
        f.close()

        if Account.objects.filter(usa_spending_updated=True).count() == Account.objects.count():
            Account.objects.all().update(usa_spending_updated=False)

        reporter = USASpendingReporter()
        reporter.find_spending_for_all_clients(datetime.date.today().year)
        return JsonResponse({})
