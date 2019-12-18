import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials


#TODO
class Database:
    INITIAL_FUND = "initial_fund"
    INITIAL_DATE = "initial_date"
    INTEREST_RATE = "interest_rate"
    INTEREST_TYPE = "interest_type"
    DEPOSIT_INTERVAL = "deposit_interval"
    DEPOSIT_ACCOUNT = "deposit_account"

    def __init__(self, credentials):
        self.credentials = credentials
        #TODO grab data from spreadsheet
        ting = 3

    def get_fund_data(self):
        return {
            "AccountA": {
                Database.INITIAL_FUND: "1000.00",
                Database.INITIAL_DATE: str(time.time() - 8640000),
                Database.INTEREST_RATE: "0.10",
                Database.INTEREST_TYPE: "apr",
                Database.DEPOSIT_INTERVAL: "86400",
                Database.DEPOSIT_ACCOUNT: "AccountA"
            }
        }
