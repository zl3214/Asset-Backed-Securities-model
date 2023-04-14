'''
Create a class called StructuredSecurities.
'''

from .standard_tranche import StandardTranche
import logging

class StructuredSecurities(object):
    def __init__(self, total_notional):
        self._total_national = total_notional
        self._tranche_list = []
        self._mode = 'Pro Rata'  # default mode is Pro Rata
        self._reserve_account = 0

    @property
    def reserve_amount(self):
        return self._reserve_account

    @property
    def tranche_list(self):
        return self._tranche_list

    @property
    def mode(self):
        return self._mode

    # Create a ‘factory method’ to add tranches to a StructuredSecurity object.
    # It will instantiate and add the tranche to the StructuredSecurity object’s internal list of tranches.
    # The method needs to know the tranche class, the percent of notional, the rate, and the subordination level.
    def addTranche(self, notional_percent, rate, subordination_level):
        # instantiate a new tranche
        new_tranche = StandardTranche(self._total_national * notional_percent, notional_percent, rate,
                                      subordination_level)
        # add tranche to the list
        self._tranche_list.append(new_tranche)
        self._tranche_list = sorted(self._tranche_list, key=lambda x: x.subordination_level)

    # class function that create StructuredSecurities object
    @classmethod
    def constructSecurities(cls, total_notional, notional_percents, rates, subordination_levels):
        structured_securities = StructuredSecurities(total_notional)
        for notional_percent, rate, subordination_level in zip(notional_percents, rates, subordination_levels):
            structured_securities.addTranche(notional_percent, rate, subordination_level)
        return structured_securities

    # Add a method that flags ‘Sequential’ or ‘Pro Rata’ modes on the object – more on this in a moment.
    @mode.setter
    def mode(self, imode):
        if imode not in {'Sequential', 'Pro Rata'}:
            logging.error('invalid mode. (Sequential / Pro Rata)')
        self._mode = imode

    # Add a method that increases the current time period for each tranche.
    def increaseTimePeriod(self):
        for tranche in self._tranche_list:
            tranche.increaseTimePeriod()

    # Create a method called makePayments. This should have a cash_amount parameter.
    # Cycle through all the tranches, in order of subordination.
    def makePayments(self, cash_amount):
        cash_left = cash_amount + self._reserve_account  # reserve account is added to cash amount
        self._reserve_account = 0  # reset reserve account to 0
        # It should cycle through all interest payments first, paying each tranche from the available cash_amount.
        for tranche in self._tranche_list:
            if tranche.current_notional_balance > 0:
                cash_left = tranche.makeInterestPayment(cash_left)
        # make principal payment second
        if cash_left > 0:
            if self._mode == 'Sequential':
                for tranche in self._tranche_list:
                    if tranche.current_notional_balance > 0 and cash_left > 0:
                        cash_left = tranche.makePrincipalPayment(cash_left)
            elif self._mode == 'Pro Rata':
                temp_cash_left = 0
                for tranche in self._tranche_list:
                    if tranche.current_notional_balance > 0:
                        # never overpay tranche balance, keep the extra cash
                        temp_cash_left += tranche.makePrincipalPayment(tranche.notional_percent * cash_left)
                cash_left = temp_cash_left
        # if there exist at least one tranche which are not fully paid, we will update the reserve account
        for tranche in self._tranche_list:
            if tranche.current_notional_balance > 0:
                self._reserve_account = cash_left

    # Create a function called getWaterfall that returns a list of lists. Each inner list represents a tranche,
    # and contains Interest Due, Interest Paid, Interest Shortfall, Principal Paid, Balance for a given time period.
    def getWaterfall(self):
        res = [[] for tranche in self._tranche_list]  # list of tranche
        for i, tranche in enumerate(self._tranche_list):
            interest_due = tranche.interestDue
            interest_paid = tranche.interestPaid
            interest_shortfall = tranche.interestShortfall
            principal_paid = tranche.principalPaid
            balance = tranche.current_notional_balance
            res[i] = [interest_due, interest_paid, interest_shortfall, principal_paid, balance]
        return res

    def reset(self):
        self._reserve_account = 0
        for tranche in self._tranche_list:
            tranche.reset()
