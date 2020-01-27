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

        fiscal_years = [year for year in range(fiscal_year-2, fiscal_year+1)]
        awards = {}
        for year in fiscal_years:
            awards[year] = {}

        spending_info = self.get_spending_info(duns_id, fiscal_years, awards)
        if not spending_info:
            spending_info = "None"
        else:
            spending_info = json.dumps(self.to_dollars(spending_info))
        self.sf.Account.update(sf_id, {'USA_Spending__c': spending_info})

    def to_dollars(self, spending_dict):
        for fiscal_year in spending_dict:
            for agency in spending_dict[fiscal_year]:
                for sub_agency in spending_dict[fiscal_year][agency]:
                    spending_dict[fiscal_year][agency][sub_agency] = '${:,.2f}'.format(spending_dict[fiscal_year][agency][sub_agency])
        return spending_dict

    def get_spending_info(self, duns_id, fiscal_years, awards, page=1):
        spending_search_url = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'
        time_periods = []
        for fiscal_year in fiscal_years:
            time_periods.append({"start_date": "{}-10-01".format(fiscal_year-1),
                                 "end_date": "{}-09-30".format(fiscal_year)})
        request_param = {"filters":
                         {"time_period": time_periods,
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

    def determine_fiscal_year(self, action_date):
        action_date = datetime.strptime(action_date,'%Y-%m-%d')
        bottom_date = datetime.strptime("{}-10-01".format(action_date.year-1),'%Y-%m-%d')
        top_date = datetime.strptime("{}-09-30".format(action_date.year),'%Y-%m-%d')

        if action_date >= bottom_date and action_date <= top_date:
            return action_date.year
        if action_date > top_date:
            return action_date.year + 1

    def consolidate_awards(self, results, awards):
        award_details_url = 'https://api.usaspending.gov/api/v2/transactions/'
        for top_award in results:
            request_param = {"award_id": top_award['generated_internal_id'],
                             "page":1,
                             "limit":100}

            award_details = json.loads(requests.post(award_details_url,
                                         json=request_param,
                                         headers={'Content-type': 'application/json'}).text)
            awarding_agency = top_award['Awarding Agency']
            sub_agency = top_award['Awarding Sub Agency']
            for award in award_details['results']:
                award_year = self.determine_fiscal_year(award['action_date'])
                amount = award['federal_action_obligation']
                if amount:
                    if award_year in awards:
                        if awarding_agency in awards[award_year]:
                            if sub_agency in awards[award_year][awarding_agency]:
                                awards[award_year][awarding_agency][sub_agency] += amount
                            else:
                                awards[award_year][awarding_agency][sub_agency] = amount
                        else:
                            awards[award_year][awarding_agency] = {sub_agency: amount}
        return awards
