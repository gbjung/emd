from django.core.management.base import BaseCommand, CommandError
from usaspending.USASpending import USASpendingReporter

class Command(BaseCommand):
    help = 'Creates a csv report of upcoming opportunities and meetings for an account'

    def add_arguments(self , parser):
        parser.add_argument('id')
        parser.add_argument('fiscal_year')

    def handle(self, *args, **options):
        account_id = options['id']
        fiscal_year = options['fiscal_year']
        reporter = USASpendingReporter()
        reporter.find_spending_for_client(account_id, int(fiscal_year))
        print("Done!")
