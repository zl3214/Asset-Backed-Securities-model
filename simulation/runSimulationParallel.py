''''
RunSimulationParallel() function
'''
import numpy as np
from doWaterfall import doWaterfall
from simulation.runSimulation import runSimlutation
from timer import Timer
from loan.loan_pool import LoanPool
from tranche.structured_securities import StructuredSecurities
import multiprocessing
import numpy


# doWork function can be any function with any argument
def doWork(input, output):
    f, args = input.get(timeout=1)
    res = f(*args)
    output.put(res)



def runSimulationParallel(loan_pool, structured_securities, NSIM, num_processes):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # add 20 runMC function items into input_queue
    for i in range(num_processes):
        input_queue.put((runSimlutation, (loan_pool, structured_securities, NSIM / num_processes)))
        # create 5 child processes
    for i in range(num_processes):
        p = multiprocessing.Process(target=doWork, args=(input_queue, output_queue))
        p.start()
        print(p)

    res = []  # result
    # return the result list

    r = output_queue.get()
    if len(res) <= 60:
        r = np.array(r)
        res.append(r)
    print(res)

    DIRR_AL_sum = sum(res)


    return DIRR_AL_sum / num_processes

