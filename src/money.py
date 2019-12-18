import os
import time
import math
from dao import Database
from display import Display


class Account:
    SECONDS_IN_DAY = 86400
    SECONDS_IN_YEAR = 31536000
    APR_INTEREST_TYPE = "apr"
    SIMPLE_INTEREST_TYPE = "simple"
    NONE_INTEREST_TYPE = "none"

    def __init__(self):
        self.account_name = ""
        self.initial_fund = 0
        self.initial_date = time.time()
        self.interest_rate = 0
        self.deposit_account = self
        self.deposit_interval_length = Account.SECONDS_IN_DAY
        self.interest_type = Account.APR_INTEREST_TYPE
        self.current_fund = 0
        self.current_date = 0

    def init(self):
        self.current_date = self.initial_date
        self.current_fund = self.initial_fund
        self.interest_type = self.interest_type.lower()

    def tick(self, target_date):
        pass
        #TODO add value to own account based off time passed
        # and deposit_account if time overflows interval

    def apply_interest(self, duration):
        if self.interest_type == Account.APR_INTEREST_TYPE:
            self.current_fund = (self.current_fund *
                                 math.pow((1 + self.interest_rate),
                                          duration/Account.SECONDS_IN_YEAR))
        elif self.interest_type == Account.SIMPLE_INTEREST_TYPE:
            self.current_fund = (self.current_fund +
                                 (self.initial_fund *
                                  self.interest_rate *
                                  duration/Account.SECONDS_IN_YEAR))

def main():
    credentials = load_cached_credentials()
    display = Display()
    if credentials is None:
        credentials = display.input(string="Enter credentials")
        save_cached_credentials(credentials)

    database = Database(credentials)
    fund_data = database.get_fund_data()
    accounts = {}
    for account_name in fund_data:
        account = Account()
        account_data = fund_data.get(account_name)
        account.account_name = account_name
        account.initial_fund = float(account_data.get(Database.INITIAL_FUND))
        account.initial_date = int(account_data.get(Database.INITIAL_DATE))
        account.deposit_interval_length = int(account_data.get(Database.DEPOSIT_INTERVAL))
        account.interest_rate = float(account_data.get(Database.INTEREST_RATE))
        account.interest_type = account_data.get(Database.INTEREST_TYPE)
    for account_name in fund_data:
        deposit_account_name = fund_data.get(account_name).get(Database.DEPOSIT_ACCOUNT)
        if deposit_account_name:
            accounts.get(account_name).deposit_account = accounts.get(deposit_account_name)

    deposit_intervals = []
    for account in accounts:
        deposit_interval = account.deposit_interval_length
        if deposit_interval not in deposit_intervals:
            deposit_intervals.append(deposit_interval)
    tick_interval = get_least_common_multiple(deposit_intervals)
    initial_date = min([account.initial_date for account in accounts])



def load_cached_credentials():
    credentials = None
    #TODO load credentials from a file
    return credentials

def save_cached_credentials(credentials):
    #TODO
    pass


def get_least_common_multiple(values):
    #TODO
    pass


if __name__ == '__main__':
    main()