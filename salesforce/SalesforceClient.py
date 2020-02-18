from simple_salesforce import Salesforce
from django.conf import settings
from accounts.models import Account
from contacts.models import Contact

class SalesforceClient:
    def __init__(self):
        self.sf = self.establish_connection()

    def establish_connection(self):
        return Salesforce(username=settings.SF_USERNAME,
                          instance_url=settings.SF_URL,
                          password=settings.SF_PW,
                          security_token=settings.SF_TOKEN)

    def import_accounts(self, sync_contacts=True):
        contacts_query = ', (select id, FirstName, LastName, MiddleName, Title from Contacts)' if sync_contacts else ''
        query_string = ('SELECT Id, Name, Unqualified__c, Cage_Code__c, DUNS_Number__c'+ contacts_query +
                        ' FROM Account where (Cage_Code__c != null and Unqualified__c = False)')

        results = self.sf.query(query_string)
        self.sync_accounts(results.get('records', []), sync_contacts)
        while not results['done']:
            next_set = self.sf.query_more(results['nextRecordsUrl'], True)
            self.sync_accounts(results.get('records', []), sync_contacts)
            results = next_set

    def sync_accounts(self, raw_accounts, sync_contacts):
        for ac in raw_accounts:
            account, created = Account.objects.update_or_create(
                                             defaults={'sf_id':ac['Id']},
                                             sf_id=ac['Id'],
                                             account_name=ac['Name'],
                                             unqualified=ac['Unqualified__c'],
                                             cage_code=ac['Cage_Code__c'],
                                             duns_number=ac['DUNS_Number__c'])
            if sync_contacts:
                self.sync_contacts(account, ac['Contacts'])

    def sync_contacts(self, account, raw_contacts):
        if not raw_contacts:
            return

        for ct in raw_contacts.get('records', []):
            Contact.objects.update_or_create(
                                   defaults={'sf_id':ct['Id']},
                                   sf_id=ct['Id'],
                                   first_name=ct['FirstName'],
                                   last_name=ct['LastName'],
                                   middle_name=ct['MiddleName'],
                                   title=ct['Title'],
                                   account=account)

    def unqualify_accounts(self):
        accounts = Account.objects.filter(sf_updated=False,
                                          sam_checked=True,
                                          unqualified=True)
        to_iterate = (accounts.count()//500)+1
        pointer = 0
        for i in range(0, to_iterate):
            print('updating {}/{}'.format(i, to_iterate))
            account_window = accounts[pointer:pointer+500]
            if account_window:
                data = [{'Id': ac.sf_id, 'Unqualified__c': True} for ac in account_window]
                self.sf.bulk.Account.upsert(data, 'Id')
                Account.objects.filter(pk__in=account_window).update(sf_updated=True)
                pointer += 500
