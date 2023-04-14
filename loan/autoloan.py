'''
Classes related to auto loan.
'''

from .loans import FixedRateLoan
from .asset.car_base import Car
import logging


# fixed rate autoloan class derived from FixedRateLoan
class AutoLoan(FixedRateLoan):
    # save car parameter as a Car object,
    # if not, print an error message and leave the function
    def __init__(self, term, rate, face, car):
        if not isinstance(car, Car):
            logging.error('input {} is not Car object.'.format(car))
            raise TypeError('Car parameter should be Car object.')
        super(AutoLoan, self).__init__(term, rate, face, car)
