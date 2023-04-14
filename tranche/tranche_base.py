'''
Create a tranche base class
'''

from functools import reduce
import numpy as np
import numpy_financial as npf

# Create an abstract base class called Tranche. It should be initialized with notional and rate.
# Additionally, it should have a subordination flag.
class Tranche(object):
    def __init__(self, notional, notional_percent, rate, subordination_level):
        self._notional = notional
        self._rate = rate
        self._subordination_level = subordination_level
        self._notional_percent = notional_percent

    @property
    def notional(self):
        return self._notional

    @property
    def rate(self):
        return self._rate

    @property
    def notional_percent(self):
        return self._notional_percent

    @property
    def subordination_level(self):
        return self._subordination_level

    @notional.setter
    def notional(self, inotional):
        self._notional = inotional

    @notional_percent.setter
    def notional_percent(self, inotional_percent):
        self._notional_percent = inotional_percent

    @rate.setter
    def rate(self, irate):
        self._rate = irate

    @subordination_level.setter
    def subordination_level(self, isubordination_level):
        self._subordination_level = isubordination_level

    # function to return internal rate of return (IRR)
    def IRR(self, monthly_payments):
        return npf.irr([-self.notional] + monthly_payments) * 12  # covert to annual IRR

    # function to calculate Average Life (AL)
    def AL(self, monthly_payments):
        payment_periods = [i + 1 for i in range(len(monthly_payments))]
        lst = zip(payment_periods,monthly_payments)
        return reduce(lambda al, zip: al + zip[0]*zip[1], lst, 0) / self.notional

    # function to calculate Reduction in Yield (DIRR)
    def DIRR(self, monthly_payments):
        return self.IRR(monthly_payments) - self.rate

    # class level lists used for ABS rating convert
    DIRRs_BPS = np.array(
        [-np.inf, 0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19, 27, 46, 72, 106, 143, 183, 231, 311, 2500, 10000])
    ABS_letter_ratings = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3",
                          "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa", "Ca"]

    # class level function to translate dirr value to a letter rating
    @classmethod
    def ABSRating(cls, dirr):
        index = np.where(cls.DIRRs_BPS >= dirr * 10000.0)[0][0] - 1  # convert DIRR to basis points
        return cls.ABS_letter_ratings[index]

    # class level function to calculate yield for each tranche
    @classmethod
    def calculateYield(cls, dirr, wal):
        return (7 / (1 + 0.08 * np.exp(-0.19 * wal / 12.0)) + 0.019 * np.sqrt(wal * dirr * 100 / 12.0)) / 100.0

    # function to update tranche rates for monte carlo simulation
    @classmethod
    def newTrancheRate(cls, old_rates, coeffs, yields):
        return old_rates + coeffs * (yields - old_rates)

    # function to update the difference for monte carlo simulation
    @classmethod
    def diff(cls, tranche_percents, last_rates, new_rates):
        return np.dot(tranche_percents, np.abs((last_rates - new_rates) / last_rates))