from django.core.management.base import BaseCommand, CommandError
from salesforce.SalesforceClient import SalesforceClient

class Command(BaseCommand):
    help = 'Creates Accounts and Contacts from Salesforce'

    def add_arguments(self , parser):
        parser.add_argument('--contacts', action='store_true')

    def handle(self, *args, **options):
        add_contacts = options['contacts']
        print(add_contacts)
        sf_client = SalesforceClient()
        sf_client.import_accounts(add_contacts)
        print('done!')
