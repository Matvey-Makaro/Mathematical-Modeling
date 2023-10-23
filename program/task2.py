import numpy as np
import sympy as sp
import random
import math
from statistical_research import *
from RVGenerator import *
import matplotlib.pyplot as plt
import copy
from collections import Counter


def generate_rv(matrix) -> tuple:
    val_x = random.uniform(0, 1)
    x_p = [sum(matrix[i]) for i in range(len(matrix))]
    x = 0
    curr_p = 0
    for i in range(len(x_p)):
        curr_p += x_p[i]
        if val_x <= curr_p:
            x = i
            break

    y_p = matrix[x]
    val_y = random.uniform(0, sum(y_p))
    curr_p = 0
    y = 0
    for i in range(len(y_p)):
        curr_p += y_p[i]
        if val_y <= curr_p:
            y = i
            break
    return x, y


def is_independent(matrix: list, x_p: list, y_p: list) -> bool:
    for i in range(len(x_p)):
        for j in range(len(y_p)):
            if not math.isclose(matrix[i][j], x_p[i] * y_p[j]):
                return False
    return True


def calc_x_if_y(matrix: list, y_p: list) -> list:
    x_if_y = copy.deepcopy(matrix)
    for j in range(len(y_p)):
        for i in range(len(matrix)):
            x_if_y[i][j] /= y_p[j]
    return x_if_y


def calc_y_if_x(matrix: list, x_p: list) -> list:
    y_if_x = copy.deepcopy(matrix)
    for i in range(len(x_p)):
        for j in range(len(matrix[0])):
            y_if_x[i][j] /= x_p[i]
    return y_if_x


def discrete_expectation(x_p: list) -> float:
    expectation = 0
    for i in range(len(x_p)):
        expectation += i * x_p[i]
    return expectation


def discrete_dispersion(x_p: list) -> float:
    mean = discrete_expectation(x_p)
    mean_square = 0
    for i in range(len(x_p)):
        mean_square += i * i * x_p[i]
    return mean_square - mean**2


def discrete_cov(matrix, x_p, y_p) -> float:
    cov = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            cov += matrix[i][j] * i * j
    cov -= discrete_expectation(x_p) * discrete_expectation(y_p)
    return cov


def discrete_correlation(matrix, x_p, y_p) -> float:
    cov = discrete_cov(matrix, x_p, y_p)
    return cov / (pow(discrete_dispersion(x_p), 1/2) * pow(discrete_dispersion(y_p), 1/2))

def task2():
    # matrix = [[0.18, 0.12],
    #           [0.24, 0.16],
    #           [0.18, 0.12]]

    matrix = [[0.18, 0.02, 0.1],
              [0.20, 0.16, 0.04],
              [0.10, 0.12, 0.08]]

    x_p = [sum(matrix[i]) for i in range(len(matrix))]
    print("x_p: ", x_p)
    y_p = []
    for j in range(len(matrix[0])):
        curr_p = 0
        for i in range(len(matrix)):
            curr_p += matrix[i][j]
        y_p.append(curr_p)

    print("y_p:", y_p)

    if not is_independent(matrix, x_p, y_p):
        print("Составляющие двумерной ДСВ зависимы")
    else:
        print("Составляющие двумерной ДСВ независимы")

    x_if_y = calc_x_if_y(matrix, y_p)
    print("x_if_y:", x_if_y)
    y_if_x = calc_y_if_x(matrix, x_p)
    print("y_if_x:", y_if_x)

    num_of_vals_to_generate = 10000
    x_values = []
    y_values = []
    for _ in range(num_of_vals_to_generate):
        x, y = generate_rv(matrix)
        x_values.append(x)
        y_values.append(y)

    x_counts = Counter(x_values)
    x_counts = dict(sorted(x_counts.items()))
    y_counts = Counter(y_values)
    y_counts = dict(sorted(y_counts.items()))

    plt.bar(list(x_counts.keys()), list(x_counts.values()), color='red')
    plt.xticks([i for i in range(len(x_p))])
    plt.show()
    plt.bar(list(y_counts.keys()), list(y_counts.values()), color='green')
    plt.xticks([i for i in range(len(y_p))])
    plt.show()

    M_x = discrete_expectation(x_p)
    M_y = discrete_expectation(y_p)
    print("M_x:", M_x)
    print("M_y", M_y)

    D_x = discrete_dispersion(x_p)
    D_y = discrete_dispersion(y_p)
    print("D_x:", D_x)
    print("D_y:", D_y)

    r = discrete_correlation(matrix, x_p, y_p)
    print("r:", r)

    stat_M_x = calc_statistical_mean(x_values)
    stat_M_y = calc_statistical_mean(y_values)
    print("stat_M_x:", stat_M_x)
    print("stat_M_y:", stat_M_y)

    stat_D_x = calc_dispersion(x_values)
    stat_D_y = calc_dispersion(y_values)
    print("stat_D_x:", stat_D_x)
    print("stat_D_y:", stat_D_y)

    stat_r = calc_correlation(x_values, y_values)
    print("stat_r: ", stat_r)
