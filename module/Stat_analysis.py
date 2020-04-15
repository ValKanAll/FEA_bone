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

Hypothesis A4: esp[i] normalised
esp[i] follow N(0, sigma^2)
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


def linear_regression_coef(x, y):
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
        x, y : real data
        X, Y : linearized data
        y_approx : regression law applied to x
        Y_approx : regression law applied to X
        '''
        if self.model == 'power':
            self.X = np.log(self.x)
            self.Y = np.log(self.y)
            self.b, a_temp = linear_regression_coef(self.X, self.Y)
            self.a = np.exp(a_temp)
            self.eps = []
            self.y_approx = []
            self.Y_approx = []
            for k in range(self.n):
                self.eps.append(self.y[k] - self.a * self.x[k] ** self.b)
                self.y_approx.append(self.a * self.x[k] ** self.b)
                self.Y_approx.append(self.b * self.X[k] + a_temp)

        if self.model == 'linear':
            self.X = self.x
            self.Y = self.y
            self.a, self.b = linear_regression_coef(self.X, self.Y)
            self.eps = []
            self.y_approx = []
            self.Y_approx = []
            for k in range(self.n):
                self.eps.append(self.y[k] - self.a * self.x[k] - self.b)
                self.y_approx.append(self.a * self.x[k] + self.b)
                self.Y_approx.append(self.a * self.X[k] + self.b)

    def get_correlation(self):
        return coef_correlation(self.X, self.Y)

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
            return 'y = ' + str(np.round(self.a, decimals=4)) + ' * x + ' + str(np.round(self.b, decimals=4))

        if self.model == 'power':
            return 'y = ' + str(np.round(self.a, decimals=4)) + ' * x ^ ' + str(np.round(self.b, decimals=4))

    def get_sigma2(self):
        sigma2 = 0
        for el in self.eps:
            sigma2 += el ** 2
        sigma2 /= (self.n - 2)
        return sigma2

    def get_R2(self):
        return var(self.Y_approx)/var(self.Y)

    def plot(self):
        min_x = np.min(self.x)
        max_x = np.max(self.x)
        t = np.linspace(min_x, max_x, 500)
        fun_law = self.get_law()
        law_t = fun_law(t)
        legend = self.get_str_law() + '\n'\
            + 'R2 = ' + str(self.get_R2()) + '\n'\
            + 'sigma^2 = ' + str(self.get_sigma2())

        plt.figure()
        plt.scatter(self.x, self.y, color='black', marker='+')
        plt.plot(t, law_t, label=legend)
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()


class DataAnalysis:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.regressions = []

    def regression(self, model='linear'):
        self.regressions.append(Regression(self.x, self.y, model))
        return 0

    def plot(self):
        min_x = np.min(self.x)
        max_x = np.max(self.x)
        t = np.linspace(min_x, max_x, 500)

        plt.figure()
        plt.scatter(self.x, self.y, color='black', marker='+')

        for regression in self.regressions:
            plt.scatter(self.x, regression.y_approx)
            fun_law = regression.get_law()
            law_t = fun_law(t)
            legend = regression.get_str_law() + '\n' \
                + 'R2 = ' + str(np.round(regression.get_R2(), decimals=4)) + '\n' \
                + 'sigma = ' + str(np.round(np.sqrt(regression.get_sigma2()), decimals=4))
            plt.plot(t, law_t, label=legend)
            plt.legend()

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()


x0 = [28, 50, 55, 110, 60, 48, 70]
y0 = [130, 280, 268, 500, 320, 250, 400]
analyse = DataAnalysis(x0, y0)
analyse.regression('linear')
analyse.regression('power')
analyse.plot()
