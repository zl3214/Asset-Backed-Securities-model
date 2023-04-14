'''
Create a LoanPool class
'''

import numpy as np
from loan.loan_base import *
from functools import reduce

class LoanPool(object):
    def __init__(self, loans):
        self._loans = loans

    @property
    def loans(self):
        return self._loans

    # method to get total loan principal
    def totalPrincipal(self):
        return sum(loan._face for loan in self._loans)

    # method to get total loan balance for a given period
    def totalBalance(self, period):
        return sum(loan.balance_formula(period) for loan in self._loans)

    # method to get aggregate principal due in a given period
    def totalPrincipalDue(self, period):
        return sum(loan.principalDue_formula(period) for loan in self._loans)

    # method to get aggregate interest in a given period
    def totalInterestDue(self, period):
        return sum(loan.interestDue_formula(period) for loan in self._loans)

    # method to get aggregate total payment in a given period
    def totalPaymentDue(self, period):
        return sum(loan.monthlyPayment(period) for loan in self._loans)

    # method to return number of active loan
    # active loans have balances greater than 0
    def numOfActive(self, period):
        loan_bals = [loan.balance_formula(period)  for loan in self._loans]
        loan_bals = list(filter(None,loan_bals))
        return len([i for i in loan_bals if i > 0])

    # method to compute WAR
    def WAR(self):
        numerator = sum(loan._face * loan._rate for loan in self._loans)
        denominator = sum(loan._face for loan in self._loans)
        return numerator / denominator

    # method to computer WAM
    def WAM(self):
        numerator = sum(loan._face * loan._term * 1.0 for loan in self._loans)
        denominator = sum(loan._face for loan in self._loans)
        return numerator / denominator

    # function to compute WAM with reduce()
    def WAM_reduce(self):
        term_list = [loan._term for loan in self._loans]  # create a list of term
        face_list = [loan._face for loan in self._loans]  # crate a list of amount
        return reduce(fn, zip(face_list, term_list), 0) / sum(face_list)

    # function to compute WAR with reduce()
    @property
    def WAR_reduce(self):
        rate_list = [loan._rate for loan in self._loans]  # create a list of rate
        face_list = [loan._face for loan in self._loans]  # crate a list of amount

        def function(total, face, rate):
            return total + face * rate

        return reduce(function, zip(face_list, rate_list), 0) / sum(face_list)

    # using __iter__ method to make LoanPool class iterable
    def __iter__(self):
        return iter(self._loans)

    # getwaterfall function
    def getWaterfall(self, period):
        res = []
        for loan in self._loans:
            res.append(
                [loan.monthlyPayment(period), loan.principalDue_formula(period), loan.interestDue_formula(period),
                 loan.balance_formula(period)])
        return res

    # check defaults function
    def checkDefaults(self, period):
        # unify the time period in a certain time period have the same interval index
        default_prob_index = np.where(period <= Loan.default_time_periods)[0][0]
        # obtain default prob for that certain period
        default_prob = Loan.default_probabilities[default_prob_index]
        # instead create uniform random integers for each loan, I just generate a uniform distribution
        # probability for each loan and check whether the probability is smaller than the default probability
        # if it is, return 0 indicating default happens, 1 otherwise.
        default_list = np.asarray(np.random.uniform(size=len(self._loans)) > default_prob, dtype=int)
        recovery_value = 0
        for loan, default_flag in zip(self._loans, default_list):
            if not loan.defaulted:  # check only when defaulted flag is false
                loan.checkDefault(default_flag)  # update the loan default status
                if loan.defaulted:  # if loan is default, return the recovery value of the asset
                    recovery_value += loan.recoveryValue(period)
        return recovery_value  # return all the defaulted loan's asset recovery value

    # reset function
    def reset(self):
        for loan in self._loans:
            loan.reset()


# global function as callable in WAM_reduce()
def fn(total, face, term):
    return total + face * term * 1.0
