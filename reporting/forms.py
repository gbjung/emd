from django import forms
from salesforce.SalesforceClient import SalesforceClient

class ReportForm(forms.Form):
    sf_id = forms.CharField()

    # def clean(self):
    #     cleaned_data = super(ReportForm, self).clean()
    #     sf_id = cleaned_data.get('sf_id')
    #     sfc = SalesforceClient()
    #     try:
    #         sf_return = sfc.sf.Account.get(sf_id)
    #     except:
    #         raise forms.ValidationError('No matching Salesforce ID')
