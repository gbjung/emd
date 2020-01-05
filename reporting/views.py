from django.shortcuts import render
from django.http import HttpResponse
from subprocess import Popen

from django.views.generic import TemplateView, FormView
from reporting.forms import ReportForm
from reporting.ReportGenerator import ReportGenerator

class ReportingView(FormView):
    template_name = 'report.html'
    success_url = 'success'
    form_class = ReportForm

    def form_valid(self, form):
        sf_id =  form.cleaned_data.get('sf_id')
        generator = ReportGenerator()
        file_name = generator.generate_report(sf_id)

        with open("%s" % file_name, "rb") as excel:
            data = excel.read()

        Popen("rm %s" % file_name, shell=True)

        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response

class SuccessView(TemplateView):
    template_name = 'report_success.html'
