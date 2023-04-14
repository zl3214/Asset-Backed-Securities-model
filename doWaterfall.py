'''
Create a standalone function called doWaterfall.
'''
from tranche.structured_securities import StructuredSecurities
from loan.loan_pool import LoanPool
import logging
from tranche.tranche_base import Tranche


# Create a standalone function called doWaterfall. This function should take two parameters:
# A LoanPool object and a StructuredSecurities object.
def doWaterfall(loan_pool, structured_securities):
    if not isinstance(loan_pool, LoanPool) or not isinstance(structured_securities, StructuredSecurities):
        logging.error('Invalid input type')
    else:
        period = 1  # start from period 1
        structured_securities_waterfall = []
        loan_pool_waterfall = []
        reserve_account_waterfall = []
        # print(loan_pool.numOfActive(1))
        while loan_pool.numOfActive(period) > 0:
            cash_amount = loan_pool.totalPaymentDue(period)  # cash amount from loan payment
            recovery_value = loan_pool.checkDefaults(period)  # check defaults and return recovery value
            # pay securities using loan payment and recovery value of default loans
            structured_securities.makePayments(cash_amount + recovery_value)
            # add security waterfall current period
            structured_securities_waterfall.append(structured_securities.getWaterfall())
            # add loan pool waterfall current period
            loan_pool_waterfall.append(loan_pool.getWaterfall(period))
            # add reserve account current period
            reserve_account_waterfall.append(structured_securities.reserve_amount)
            structured_securities.increaseTimePeriod()  # update time period
            period += 1

        tranche_payments = [[] for i in range(len(structured_securities.tranche_list))]
        for period_waterfall in structured_securities_waterfall:
            for tranche_index, tranche_waterfall in enumerate(period_waterfall):
                tranche_payments[tranche_index].append(tranche_waterfall[1] + tranche_waterfall[3])
        tranche_metrics = [(tranche.IRR(payments), tranche.DIRR(payments), tranche.AL(payments),
                            Tranche.ABSRating(tranche.DIRR(payments))) for tranche, payments in
                           zip(structured_securities.tranche_list, tranche_payments)]

        return loan_pool_waterfall, structured_securities_waterfall, reserve_account_waterfall,tranche_metrics
