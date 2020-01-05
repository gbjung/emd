from django.core.management.base import BaseCommand, CommandError
from reporting.ReportGenerator import ReportGenerator

class Command(BaseCommand):
    help = 'Creates a csv report of upcoming opportunities and meetings for an account'

    def add_arguments(self , parser):
        parser.add_argument('id')

    def handle(self, *args, **options):
        account_id = options['id']
        generator = ReportGenerator()
        generator.generate_report(account_id)
        print("Done!")
