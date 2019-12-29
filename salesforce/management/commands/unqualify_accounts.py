from django.core.management.base import BaseCommand, CommandError
from salesforce.SalesforceClient import SalesforceClient

class Command(BaseCommand):
    help = 'Syncs unqualified accounts with Salesforce'

    def handle(self, *args, **options):
        sf_client = SalesforceClient()
        sf_client.unqualify_accounts()

        print('done!')
