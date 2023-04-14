
import csv
from loan.loan_pool import LoanPool
from loan.loan_base import *
from loan.autoloan import AutoLoan
from loan.asset.cars import *
from tranche.structured_securities import StructuredSecurities
from doWaterfall import doWaterfall
import itertools

def main():
    l = Lamborghini(100000)
    lp = LoanPool([Loan(100,0.05,24,l),Loan(100,0.05,24,l),Loan(100,0.05,12,l)])
    print(lp.numOfActive(20))




if __name__ == '__main__':
    main()