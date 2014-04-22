import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def plot_losses(timeVec, lossVec, bestTime = None, timeWindowLen = None):

    plt.plot(timeVec, lossVec, 'o')

    plt.xlabel('Time')
    plt.ylabel('Loss')

    minX = 2*timeVec[0]-timeVec[1]
    minY = min(lossVec)*0.9
    plt.xlim(xmin=minX)  # padding
    plt.ylim(ymin=minY)
    title = 'Losses on A Timeline'


    # time window
    if bestTime is not None:
        plt.axvspan(bestTime, bestTime + timeWindowLen - 1, facecolor='g', alpha=0.5)
        title += ' (Time Window = ' + str(timeWindowLen) + ')'

    plt.title(title)
    plt.show()


def simulate_times(expiration, numLosses, method, verbose=True):
    """
    simulate the loss timeline
    time distribution: equal intervals
    @param method: controls the distribution of time points. is one of:
        "even": evenly spread out
        "unif": uniform random
        "poisson": poisson distribution
    @returns: timeVec
    """

    assert method in ['even', 'unif', 'poisson']

    timeVec = None

    if method == 'even':
        interval = 1. * expiration / numLosses
        timeVec = np.arange(start=0, stop=expiration, step=interval).round()    # whole days only

    elif method == 'unif':
        timeVec = np.sort(np.random.randint(low=0, high=expiration, size=numLosses))

    elif method == 'poisson':
        temp = np.random.exponential(expiration/numLosses, numLosses).cumsum()  # simulate
        timeVec = (temp / max(temp) * expiration).round()    # scale and round

    assert len(timeVec) == numLosses

    if verbose:
        print timeVec

    return timeVec


def simulate_losses(numLosses, minLoss, maxLoss, method, sd=0, verbose=True):
    """
    simulate losses
    loss distribution: uniform random
    @param method: one of:
        "uniform": Unif[minLoss, maxLoss]
        "monoDec": monotonically decreasing from maxLoss to minLoss with white noise N(0, sd)
        "monoInc": monotonically increasing from minLoss to maxLoss with white noise N(0, sd)
        "bell" : bell shaped between minLoss and maxLoss with white noise N(0, sd)
    @param sd: standard deviation of the white noise term
    @returns: lossVec
    """

    assert method in ['uniform', 'monoDec', 'monoInc', 'bell']

    noises = np.random.normal(0, sd, size=numLosses) if sd>0 else [0]*numLosses

    if method == 'uniform':     # Unif[minLoss, maxLoss]
        means = np.random.uniform(low=minLoss, high=maxLoss, size=numLosses)

    elif method == 'monoDec':   # monotonically decreasing from maxLoss to minLoss with white noise N(0, sd)
        means = np.arange(start=maxLoss, stop=minLoss, step=-1.*(maxLoss-minLoss)/numLosses)

    elif method == 'monoInc':   # monotonically decreasing from maxLoss to minLoss with white noise N(0, sd)
        means = np.arange(start=minLoss, stop=maxLoss, step=1.*(maxLoss-minLoss)/numLosses)

    elif method == 'bell':  # bell shaped between minLoss and maxLoss with white noise N(0, sd)
        means = (maxLoss - minLoss) * norm.pdf(np.linspace(start=-3, stop=3, num=numLosses)) + minLoss

    lossVec = means + noises

    assert len(lossVec) == numLosses

    if verbose:
        print lossVec

    return lossVec


def find_window(windowLen, treatyFunc, verbose):
    """
    find the optimal window given losses on a timeline
    @returns: bestTime, maxPayout
    """

    maxPayout = 0
    bestTime = None
    for i, t in enumerate(timeVec):
        curTimes = timeVec[i:] < t + windowLen
        curLosses = lossVec[i:][curTimes]
        payout = treatyFunc(curLosses)

        # printing
        if verbose >= 2:
            print '---- t =', t
            if verbose >= 3:
                print 'curTimes:', curTimes
                print 'curLosses:', curLosses
            print 'payout:', payout

        if payout > maxPayout:

            if verbose >= 1:
                print 'Replacing old maxPayout', maxPayout, 'with new', payout, '; new best time is', t

            maxPayout = payout
            bestTime = t

    return bestTime, maxPayout


def treaty_CatXL(deductible, limit):
    """ generates the CatXL treaty function
    @returns: a function
    """

    assert limit > deductible, 'Limit cannot be less than deductible.'

    return lambda losses: min(max(sum(losses) - deductible, 0), limit - deductible)


# -------- simulate losses on a time line ----------
expiration = 1000
numLosses = 20
minLoss = 500
maxLoss = 1000
timeDist = 'poisson'    # in ['even', 'unif', 'poisson']
lossSd = 50
lossDist = 'bell'       # in ['uniform', 'monoDec', 'monoInc', 'bell']

timeVec = simulate_times(expiration, numLosses, method=timeDist)
lossVec = simulate_losses(numLosses, minLoss, maxLoss, method=lossDist, sd=lossSd)

# -------- define the treaty ----------
deductible = 1000
limit = 2400
treatyFunc = treaty_CatXL(deductible=deductible, limit=limit)

# -------- find the optimal window ----------
windowLen = 150   # integer number of days
bestTime, maxPayout = find_window(windowLen, treatyFunc, verbose=2)
plot_losses(timeVec, lossVec, bestTime=bestTime, timeWindowLen=windowLen)



