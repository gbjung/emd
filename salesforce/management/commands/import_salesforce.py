from django.core.management.base import BaseCommand, CommandError
from salesforce.SalesforceClient import SalesforceClient

class Command(BaseCommand):
    help = 'Creates Accounts and Contacts from Salesforce'

    def handle(self, *args, **options):
        sf_client = SalesforceClient()
        sf_client.import_accounts()
        print('done!')
