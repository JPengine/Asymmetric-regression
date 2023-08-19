# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SZB6AvjfnGxqxcvavXz7fJjhyr1B6kM_
"""

import numpy as np
import scipy.stats
from scipy.optimize import minimize

# Bounds  betas, parameters for each distribution
bd_SN = [(-np.inf, np.inf),(-np.inf, np.inf),(0,np.inf),(-np.inf, np.inf)]  #b0, b1 for AR(1), sigma, lambda
bd_T = [(-np.inf, np.inf),(-np.inf, np.inf),(0,np.inf),(-np.inf, np.inf),(0,np.inf)]


def mle_regression(dist, y, x=None, initial=None, method="Nelder-Mead", bounds=None, options=None):

    if len(y) == 0:
        raise ValueError("y must be provided")

    if x is None:
        x = np.ones(len(y)).reshape(-1, 1)

    n = y.shape[0]
    p = x.shape[1]

    if dist == 'SN':
        def LL_sn(b):
            R = (2/b[p]) * scipy.stats.norm.pdf((y - np.dot(x, b[:p])) / b[p]) * scipy.stats.norm.cdf(b[p+1] * (y - np.dot(x, b[:p])) / b[p])
            return -np.sum(np.log(R))

        fit = minimize(LL_sn, initial, method=method, bounds=bounds, options=options)
        coefficient = fit.x[0:p]
        sigma = fit.x[p]
        _lambda = fit.x[p+1]
        return {"coefficient": coefficient, "sigma": sigma, "lambda": _lambda}

    elif dist == 'ST':
        def LL_t(b):
            R = 2/b[p] * scipy.stats.t.pdf(x=(y - np.dot(x, b[:p])) / b[p], df=b[p+2]) * \
                scipy.stats.t.cdf((b[p+1]*(y - np.dot(x, b[:p])) / b[p]) * \
                np.sqrt((b[p+2]+1)/(b[p+2]+((y - np.dot(x, b[:p])) / b[p])**2/b[p]**2)), df=b[p+2] + 1)
            return -np.sum(np.log(R))

        fit = minimize(LL_t, initial, method=method, bounds=bounds, options=options)
        coefficient = fit.x[0:p]
        sigma = fit.x[p]
        _lambda = fit.x[p+1]
        nu = fit.x[p+2]
        return {"coefficient": coefficient, "sigma": sigma, "lambda": _lambda, "nu": nu}

    else:
        raise ValueError("Invalid distribution type. Choose 'SN' for skew normal or 'ST' for student's t.")