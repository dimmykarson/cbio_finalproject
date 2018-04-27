import numpy as np
from scipy.optimize import minimize
x = []
y = []

def loglike_similarity(base, target):
    global x
    global y
    x = np.array(base)
    y = np.array(target)
    lik_model = minimize(lik, np.array([1, 1, 1]), method='L-BFGS-B')
    fun = lik_model.fun
    return fun*(-1)

def lik(parameters):
    m = parameters[0]
    b = parameters[1]
    sigma = parameters[2]
    for i in np.arange(0, len(x)):
        y_exp = m * x + b
    L = (len(x)/2 * np.log(2 * np.pi) + len(x)/2 * np.log(sigma ** 2) + 1 /
         (2 * sigma ** 2) * sum((y - y_exp) ** 2))
    return L

