import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.stats import chi2, poisson, t


def cmp_float(lhs, rhs):
    return math.fabs(lhs - rhs) < 0.001


def check_distr_func(distr_func, var, low, high) -> bool:
    low_val = float(distr_func.subs(var, low).evalf())
    if not cmp_float(low_val, 0):
        return False
    high_val = float(distr_func.subs(var, high).evalf())
    if not cmp_float(high_val, 1):
        return False
    return True


def calc_statistical_mean(values: list) -> float:
    return sum(values) / len(values)


def calc_dispersion(values: list) -> float:
    sum = 0
    m = calc_statistical_mean(values)
    for i in values:
        sum += (i - m) ** 2
    return sum / (len(values) - 1)


def create_histogram(values: list, intervals_num: int) -> None:
    plt.hist(values, bins=intervals_num)
    plt.show()


def calc_distr_density(distr_func, var):
    distr_density = distr_func.diff(var)
    return distr_density


def calc_math_expectation(distr_density, var, low, high):
    math_expectation = sp.integrate(distr_density * var, (var, low, high))
    return float(math_expectation)


def calc_theoretical_dispersion(distr_density, var, low, high):
    math_expectation = calc_math_expectation(distr_density, var, low, high)
    dispersion = float(sp.integrate((var ** 2) * distr_density, (var, low, high))) - math_expectation ** 2
    return dispersion


def calc_mean_confidence_interval(data: list, confidence_level: float) -> tuple:
    mean = calc_statistical_mean(data)
    dispersion = calc_dispersion((data))
    n = len(data)
    tmp = t.ppf(confidence_level, n - 1)
    eps = np.sqrt(dispersion) * tmp / np.sqrt(n - 1)
    return (mean - eps, mean + eps)


def calc_standard_deviation_conf_interval(data: list, confidence_level: float) -> tuple:
    mean = calc_statistical_mean(data)
    dispersion = calc_dispersion(data)
    standard_deviation = np.sqrt(dispersion)

    n = len(data)

    a1 = (1 - confidence_level) / 2.0
    a2 = (1 + confidence_level) / 2.0

    standard_deviation_left = np.sqrt((n - 1) / chi2.ppf(a2, n - 1)) * standard_deviation
    standard_deviation_right = np.sqrt((n - 1) / chi2.ppf(a1, n - 1)) * standard_deviation
    return (standard_deviation_left, standard_deviation_right)


def build_statistical_series(values: list, intervals_num: int, ):
    intervals = np.linspace(0, np.max(values), intervals_num)
    statistical_series = {(intervals[i], intervals[i + 1]): 0 for i in range(len(intervals) - 1)}
    for element in values:
        for i in range(len(intervals) - 1):
            if element >= intervals[i] and element < intervals[i + 1]:
                statistical_series[(intervals[i], intervals[i + 1])] += 1
                break
    return statistical_series


def test_hypothesis(statistical_series, distr_func, var, significance_level):
    # Хи квадрат
    n = sum(statistical_series.values())
    curr_chi2 = 0
    for key, value in statistical_series.items():
        pi = float(distr_func.subs(var, key[1]).evalf()) - float(distr_func.subs(var, key[0]).evalf())
        npi = pi * n
        curr_chi2 += ((value - npi) ** 2) / value
    crit_chi2 = chi2.ppf(1 - significance_level, len(statistical_series) - 1)
    print(f"Chi2: {curr_chi2}")
    print(f"Crit Chi2: {crit_chi2}")
    return curr_chi2 < crit_chi2


def calc_math_expectation_uniform(a: int, b: int):
    return (a + b) / 2


def calc_dispersion_uniform(a: int, b: int):
    n = b - a + 1
    return (n ** 2 - 1) / 12


def test_hypothesis_uniform(statistical_series, significance_level, a: int, b: int):
    n = sum(statistical_series.values())
    curr_chi2 = 0
    pi = 1 / (b - a + 1)
    npi = pi * n
    for key, value in statistical_series.items():
        curr_chi2 += ((value - npi) ** 2) / value
    crit_chi2 = chi2.ppf(1 - significance_level, len(statistical_series) - 1)
    print(f"Chi2: {curr_chi2}")
    print(f"Crit Chi2: {crit_chi2}")
    return curr_chi2 < crit_chi2

def calc_theor_cov(f_x_y, f_x, x, low_x, high_x, f_y, y, low_y, high_y):
    M_x = calc_math_expectation(f_x, x, low_x, high_x)
    M_y = calc_math_expectation(f_y, y, low_y, high_y)
    first_integral = sp.integrate(x * y * f_x_y, (x, low_x, high_x))
    return sp.integrate(first_integral, (y, low_y, high_y)) - M_x * M_y

def calc_theor_correlation(f_x_y, f_x, x, low_x, high_x, f_y, y, low_y, high_y):
    cov = calc_theor_cov(f_x_y, f_x, x, low_x, high_x, f_y, y, low_y, high_y)
    D_x = calc_theoretical_dispersion(f_x, x, low_x, high_x)
    D_y = calc_theoretical_dispersion(f_y, y, low_y, high_y)
    return cov / (pow(D_x, 1/2) * pow(D_y, 1/2))


def calc_correlation(x_values, y_values):
    x_y_mean = 0
    for i in range(len(x_values)):
        x_y_mean += x_values[i] * y_values[i]
    x_y_mean /= len(x_values)
    x_mean = calc_statistical_mean(x_values)
    y_mean = calc_statistical_mean(y_values)
    D_x = calc_dispersion(x_values)
    D_y = calc_dispersion(y_values)
    return (x_y_mean - x_mean * y_mean) / (pow(D_x, 1/2) * pow(D_y, 1/2))


