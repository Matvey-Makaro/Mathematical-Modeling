import matplotlib.pyplot as plt
import sympy as sp
import random
from statistical_research import *


class DiscreteUniformDistributionGenerator:
    def __init__(self, a: int, b: int):
        self._a = a
        self._b = b
        self._section_len = 1 / (self._b - self._a + 1)

    def generate(self) -> int:
        rv = random.uniform(0, 1)
        return self._a + int(rv / self._section_len)


def task2() -> None:
    random.seed(1087)
    x = sp.symbols("x")
    try:
        a = 0
        b = 10
        # a = int(input("Введите а: "))
        # b = int(input("Введите b:"))
    except Exception as ex:
        print("Incorrect input")
        return

    generator = DiscreteUniformDistributionGenerator(a, b)
    values = [generator.generate() for _ in range(1000000)]
    intervals_num = b - a + 1

    create_histogram(values, intervals_num)

    statistical_mean = calc_statistical_mean(values)
    practical_dispersion = calc_dispersion(values)

    n = b - a + 1
    distr_func = (x - a + 1) / n
    distr_density = calc_distr_density(distr_func, x)
    math_expectation = calc_math_expectation_uniform(a, b)
    theoretical_dispersion = calc_dispersion_uniform(a, b)

    print("Statistical mean: ", statistical_mean)
    print("Math expectation: ", math_expectation)
    print("Practical dispersion: ", practical_dispersion)
    print("Theoretical dispersion", theoretical_dispersion)

    print(f"Доверительный интервал для мат. ожидания: ", calc_mean_confidence_interval(values, 0.99))
    print(f"Доверительный интервал для среднеквадратичного отклонения: ",
          calc_standard_deviation_conf_interval(values, 0.99))

    statistical_series = {v: 0 for v in values}
    for v in values:
        statistical_series[v] += 1

    is_true = test_hypothesis_uniform(statistical_series, 0.7, a, b)

    if is_true:
        print("Нет оснований отвергать гипотезу о том, что генеральная совокупность распределена по "
              "данному закону распределения.")
    else:
        print("Нет оснований принять гипотезу о том, что генеральная совокупность распределена "
              "по данному закону распределения")
