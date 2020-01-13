from django.core.management.base import BaseCommand, CommandError
from usaspending.USASpending import USASpendingReporter

class Command(BaseCommand):
    help = 'Creates a csv report of upcoming opportunities and meetings for an account'

    def handle(self, *args, **options):
        reporter = USASpendingReporter()
        reporter.find_spending_for_all_clients()
        print("Done!")
