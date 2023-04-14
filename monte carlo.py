
import random
import numpy as np



def main():
    random.seed(2023)
    n = 100000

    '''Q2'''
    is_break = []
    for i in range(1,n):
        elev = []
        for j in range(1,11):
            x = random.choice(['M','F'])
            if x == 'M':
                male = random.normalvariate(5.13,0.17)
                elev.append(np.exp(male))
            else:

                female = random.normalvariate(4.96,0.2)
                elev.append(np.exp(female))


        if sum(elev) > 1750:
            is_break.append(1)
        else:
            is_break.append(0)


    # print(is_break)
    print(sum(is_break)/n)

    '''
    output: 0.05586
    After simulating 100000 times, we found the probability of break is 0.056
    '''


    '''Q3'''
    sav = np.random.normal(5,4,size=n)
    siz = np.random.normal(40000,10000,size=n)
    total = sav*siz
    print(np.mean(total))

    '''
    output: 200205.03426513515
    After simulating 100000 times, we found the average estimate of the total saving is 200205 dollars
    '''



if __name__ == '__main__':
    main()