import time
import requests
import json
from django.core.management.base import BaseCommand, CommandError
from accounts.models import Account

class Command(BaseCommand):
    help = 'Checks "System for Award Management" to see if clients are still valid'

    def make_call(self, cage_codes):
        time.sleep(.5)
        codes = ','.join(cage_codes)
        api_key = 'nwS6hhgWyoXa61Is2rw03TCxiUslXaLkqzOk6JWy'
        url = 'https://api.data.gov/sam/v3/registrations?qterms=cage:({})&api_key={}'.format(codes, api_key)
        result = json.loads(requests.get(url).content)

        return result

    def account_accounts(self, api_data, cage_codes):
        cage_map = {}
        for data in api_data:
            cage_map[data['cage']] = data

        for cage_code in cage_codes:
            accounts = Account.objects.filter(cage_code=cage_code)
            if cage_code in cage_map:
                if data['status'] != 'Active':
                    accounts.update(unqualified=True)
            else:
                accounts.update(unqualified=True)
            accounts.update(sam_checked=True)

    def handle(self, *args, **options):
        api_limit = 950
        pointer = 0
        for i in range(api_limit):
            accounts = Account.objects.filter(sam_checked=False)[:10]
            print('api limit {}/{}'.format(i, api_limit))
            cage_codes = [account.cage_code for account in accounts]
            results = self.make_call(cage_codes).get('results')
            self.account_accounts(results, cage_codes)
            pointer += 10
            print(Account.objects.filter(sam_checked=False).count())
