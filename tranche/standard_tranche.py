'''
Create a class called StandardTranche.
'''

import logging
from .tranche_base import Tranche

# # Standard tranches start off with a certain notional and need to be able to keep track of all payments made to it.
class StandardTranche(Tranche):
    def __init__(self, notional, notional_percent, rate, subordination_level):
        super(StandardTranche, self).__init__(notional, notional_percent, rate, subordination_level)
        self._current_time_period = 0
        self._current_principal_paid = 0
        self._current_notional_balance = self.notional
        self._current_interest_paid = 0
        self._current_interest_due = 0
        self._current_interest_shortfall = 0

    # They need to be able to keep track of all interest payments and all principal payments made to it, and at what time period.
    @property
    def interestDue(self):
        return self._current_interest_due

    @property
    def interestPaid(self):
        return self._current_interest_paid

    @property
    def principalPaid(self):
        return self._current_principal_paid

    @property
    def interestShortfall(self):
        return self._current_interest_shortfall

    @property
    def current_notional_balance(self):
        return self._current_notional_balance

    # increaseTimePeriod: This should increase the current time period of the object by 1 (starts from 0).
    def increaseTimePeriod(self):
        self._current_time_period += 1
        # add interest shortfall into the next interest period
        self._current_interest_due = self.rate * self._current_notional_balance + self._current_interest_shortfall
        self._current_interest_paid = 0
        self._current_principal_paid = 0
        self._current_interest_shortfall = 0

    # makePrincipalPayment: This should record a principal payment for the current object time period.
    # This should only be allowed to be called once for a given time period (raise an error otherwise)
    def makePrincipalPayment(self, cash_amount, period=1):
        if self._current_principal_paid > 0:  # positive means current principal already paid
            logging.info('Current principal is already paid.')
        elif self._current_notional_balance == 0:  # means notional already fully paid
            logging.info('Current national balance is 0. No payment is needed.')
        else:
            self._current_principal_paid = min(self._current_notional_balance,cash_amount)  # in case principal shortfall

            # notionalBalance: This should return the amount of notional still owed to the tranche for the current time period.
            self._current_notional_balance -= self._current_principal_paid
        return cash_amount - self._current_principal_paid  # return cash left

    # makeInterestPayment: This should record an interest payment for the current object time period.
    # This should only be allowed to be called once for a given time period (raise an error otherwise).
    def makeInterestPayment(self, cash_amount, period=1):
        if self._current_interest_paid > 0:  # positive means current interest already paid
            logging.info('Current interest is already paid.')
        elif self._current_interest_due == 0:  # means interest is fully paid
            logging.info('Current interest due is 0. No payment is needed.')
        else:
            self._current_interest_paid = min(self._current_interest_due, cash_amount)
            self._current_interest_shortfall = self._current_interest_due - self._current_interest_paid
        return cash_amount - self._current_interest_paid  # return cash left

    # reset: This should reset the tranche to its original state (time 0).
    def reset(self):
        self._current_time_period = 0
        self._current_principal_paid = 0
        self._current_notional_balance = self.notional
        self._current_interest_paid = 0
        self._current_interest_due = 0
        self._current_interest_shortfall = 0

