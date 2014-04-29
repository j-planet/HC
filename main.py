import matplotlib.pyplot as plt

from helpers import *





# -------- define the treaty ----------
d1Vec = [1000, 2000]
l1Vec = [2500, 4000]
d2Vec = [200, 400]
l2Vec = [500, 1000]

# -------- find the optimal window ----------
windowLen = 150   # integer number of days

expiration = 1000
numLosses = 20
minLoss = 500
maxLoss = 1000
lossSd = 50

for d1 in d1Vec:
    for l1 in l1Vec:
        for d2 in d2Vec:
            for l2 in l2Vec:

                #treatyFunc = treaty_CatXL(deductible=deductible, limit=limit)
                treatyFunc = treaty_inuring_CatXL(d1 = d1, l1 = l1, d2 = d2, l2 = l2)
                f = plt.figure(figsize=(22, 12))

                plotInd = 1
                for rowInd, timeDist in enumerate(['even', 'unif', 'poisson']):

                    timeVec = simulate_times(expiration, numLosses, method=timeDist)

                    for colInd, lossDist in enumerate(['uniform', 'monoDec', 'monoInc', 'bell']):

                        lossVec = simulate_losses(numLosses, minLoss, maxLoss, method=lossDist, sd=lossSd)

                        bestTime, _, maxPayout = find_window(windowLen, treatyFunc, timeVec, lossVec, verbose=0)

                        plt.subplot(3, 4, plotInd)
                        plot_losses(timeVec, lossVec, bestTime=bestTime, timeWindowLen=windowLen, show=False, xlabel=None,
                                    presetTitle='times ~ ' + timeDist + '; losses ~ ' + lossDist)

                        plotInd += 1

                f.suptitle('d1 = ' + str(d1) + '; l1 = ' + str(l1) + '; d2 = ' + str(d2) + '; l2 = ' + str(l2)
                           + '; Window = ' + str(windowLen))

                f.savefig('/home/jj/code/HoursClause/inuringPlots/' + '_'.join([str(d1), str(l1), str(d2), str(l2)]) + '.png')
                f.savefig('/home/jj/code/HoursClause/inuringPlots/' + '_'.join([str(d1), str(l1), str(d2), str(l2)]) + '.jpg')
                
plt.show()

