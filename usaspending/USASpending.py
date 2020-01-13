import time
import requests
import json
from datetime import datetime

from salesforce.SalesforceClient import SalesforceClient

class USASpendingReporter:
    def __init__(self):
        sfc = SalesforceClient()
        self.sf = sfc.sf

    def find_spending_for_all_clients(self, fiscal_year=datetime.now().year):
        clients = self.sf.query("SELECT Id FROM Account WHERE (Type='Client')")
        for client in clients['records']:
            print(client['Id'])
            self.find_spending_for_client(client['Id'], fiscal_year)

    def find_spending_for_client(self, sf_id, fiscal_year):
        account_info = self.sf.Account.get(sf_id)

        if not account_info:
            return None

        duns_id = account_info['DUNS_Number__c']

        if not duns_id:
            return None

        spending_info = self.get_spending_info(duns_id, fiscal_year, {})
        if not spending_info:
            spending_info = "None"
        else:
            spending_info = json.dumps(self.to_dollars(spending_info))

        self.sf.Account.update(sf_id, {'USA_Spending__c': spending_info})

    def to_dollars(self, spending_dict):
        for agency in spending_dict:
            for sub_agency in spending_dict[agency]:
                spending_dict[agency][sub_agency] = '${:,.2f}'.format(spending_dict[agency][sub_agency])
        return spending_dict

    def get_spending_info(self, duns_id, fiscal_year, awards, page=1):
        spending_search_url = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'
        request_param = {"filters":
                         {"time_period":[
                             {"start_date": "{}-10-01".format(fiscal_year-1),
                              "end_date": "{}-09-30".format(fiscal_year)}],
                          "award_type_codes":["A","B","C","D"],
                          "recipient_search_text":[duns_id]},
                          "fields":["Award ID",
                                    "Award Amount",
                                    "Awarding Agency",
                                    "Awarding Sub Agency"],
                        "page":page,
                        "limit":100,
                        "sort":"Award Amount",
                        "order":"desc",
                        "subawards":False}

        response = requests.post(spending_search_url,
                                 json=request_param,
                                 headers={'Content-type': 'application/json'})

        if response.status_code != 200:
            return awards

        response = json.loads(response.text)

        if not response['results']:
            return awards

        awards = self.consolidate_awards(response['results'], awards)

        if response['page_metadata']["hasNext"]:
            self.get_spending_info(duns_id, fiscal_year, awards=awards, page=page+1)

        return awards

    def consolidate_awards(self, results, awards):
        for award in results:
            amount = award['Award Amount']
            awarding_agency = award['Awarding Agency']
            sub_agency = award['Awarding Sub Agency']
            if awarding_agency in awards:
                if sub_agency in awards[awarding_agency]:
                    awards[awarding_agency][sub_agency] += amount
                else:
                    awards[awarding_agency] = {sub_agency: amount}
            else:
                awards[awarding_agency] = {sub_agency: amount}
        return awards
