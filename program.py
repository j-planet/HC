# Given a program (non-overlapping CatXL covers), check to see whether it's equivalent to optimize for covers
# individually or together.

import numpy as np
import random
from pprint import pprint
from helpers import simulate_times, simulate_losses, treaty_CatXL_program, treaty_CatXL, find_window


numTests = 1000

windowLen = 150   # integer number of days
expiration = 1000
numLosses = 20
minLoss = 500
maxLoss = 1000
lossSd = 50

for _ in range(numTests):
    timeVec = simulate_times(expiration, numLosses, method='poisson')
    lossVec = simulate_losses(numLosses, minLoss, maxLoss, method='monoDec', sd=lossSd)

    dVec = random.sample(xrange(1000, 4800), 4)
    dVec.sort()
    lVec = (np.array(list(dVec[1:]) + [5000]) + dVec)/2.

    # find window individually
    treaties = [treaty_CatXL(d, lVec[i]) for i, d in enumerate(dVec)]
    bestTimes_indiv = [find_window(windowLen, treaty, timeVec, lossVec, verbose=0)[1] for treaty in treaties]

    # find window together
    prog = treaty_CatXL_program(dVec, lVec)
    bestTimes_prog = find_window(windowLen, prog, timeVec, lossVec, verbose=0)[1]

    # print 'best times for individual treaties:'
    # pprint(bestTimes_indiv)
    # print 'best times for the program:', bestTimes_prog

    assert set(bestTimes_prog) <= set.intersection(*[set(ts) for ts in bestTimes_indiv])

print 'PASSED!!'