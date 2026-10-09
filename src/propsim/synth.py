import numpy as np


def synthetic_days(regimes=((120, 0.0), (120, 3.0)), daily_sd=10.0, seed=0):
    rng = np.random.default_rng(seed)
    net = np.concatenate([rng.normal(mean, daily_sd, n) for n, mean in regimes])
    low = np.minimum(net, 0.0) - np.abs(rng.normal(0, daily_sd * 0.5, len(net)))
    return net, low
