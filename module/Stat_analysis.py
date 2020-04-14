'''
The idea here is to have functions to analyse correlations between data.
y : data to be explained
x : explicative data
eps : random error
a, b : parameters to be estimated

Hypothesis A0:
y[i] is observed and random
x[i] is observed and not random
esp[i] is not observed and random

Hypothesis A1: errors are centered
E[esp[i]] = 0 for i = 1..n
E[y[i]] = 0 for i = 1..n (equivalent)

Hypothesis A2: Homogeneity of variances
Var(eps[i]) = sigma^2 for i = 1..n
Var(y[i]) = sigma^2 for i = 1..n (equivalent)

Hypothesis A3: esp[i] not correlated
Cov[esp[i], esp[j]] = 0 for i != j
Cov[esp[i], esp[j]] = 0 for i != j (equivalent)

'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def average(x):
    res = 0
    n = 0
    for el in x:
        res += el
        n += 1
    return res/n

def cov(x, y):
    n = len(x)
    if n != len(y):
        return 'error: sizes of data are not matching'
    else:
        sum_x = 0
        sum_y = 0
        prod_mixte = 0
        for i in range(n):
            prod_mixte += x[i]*y[i]
            sum_x += x[i]
            sum_y += y[i]
        return (prod_mixte - sum_x * sum_y / n) / n


def var(x):
    return cov(x, x)


def coef_correlation(x, y):
    return cov(x, y)/np.sqrt(var(x)*var(y))


def linear_coef(x, y):
    a = cov(x, y) / cov(x, x)
    b = average(y) - a * average(x)
    return a, b


class Regression:
    def __init__(self, x, y, model='linear'):
        self.model = model
        self.x = x
        self.y = y
        self.n = len(x)
        '''
        linear : y = a * x + b
        power : y = a * x ** b
        '''
        if self.model == 'power':
            self.X = np.log(self.x)
            self.Y = np.log(self.y)
            self.b, a_temp = linear_coef(self.X, self.Y)
            self.a = np.exp(a_temp)

        if self.model == 'linear':
            self.X = self.x
            self.Y = self.y
            self.a, self.b = linear_coef(self.X, self.Y)

    def get_correlation(self):
        return coef_correlation(self.x, self.y)

    def get_law(self):
        def create_fun(_a, _b, model):
            if model == 'linear':
                def fun(_x):
                    return _a * _x + _b
                return fun
            if model == 'power':
                def fun(_x):
                    return _a * _x ** _b
                return fun
        return create_fun(self.a, self.b, self.model)

    def get_str_law(self):
        if self.model == 'linear':
            return str(self.a) + ' * x + ' + str(self.b)

        if self.model == 'power':
            return str(self.a) + ' * x ^ ' + str(self.b)

    def plot(self):
        min_x = np.min(self.x)
        max_x = np.max(self.x)
        t = np.linspace(min_x, max_x, 500)
        fun_law = self.get_law()
        law_t = fun_law(t)
        legend = self.get_str_law()


        plt.figure()
        plt.scatter(self.x, self.y, color='black', marker='+')
        plt.plot(t, law_t, label=legend+'\nr = '+str(self.get_correlation()))
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()



x0 = [28, 50, 55, 110, 60, 48]
y0 = [130, 280, 268, 500, 320, 250]
Regression(x0, y0, 'power').plot()
