import matplotlib.pyplot as plt
import sympy as sp
import random
from statistical_research import *


# RV - random value
class RVGenerator:
    def __init__(self, distr_func, x, y, low, high):
        self._distr_func = distr_func
        self._x = x
        self._y = y
        self._inverse_func = None
        self._low = low
        self._high = high

        self._calc_inverse_func()


    def generate(self) -> float:
        uniform_rv = random.uniform(0, 1)
        rv = sp.simplify(self._inverse_func.subs(self._y, uniform_rv).evalf())
        return float(rv)

    def get_inverse_func(self):
        return self._inverse_func

    def _calc_inverse_func(self):
        solutions = sp.solve(self._distr_func - self._y, self._x)
        self._inverse_func = self._find_suitable_solution(solutions)
        if self._inverse_func is None:
            raise RuntimeError("Failed to find the inverse function")

    def _find_suitable_solution(self, solutions: list):
        points_to_check = [0, 0.25, 0.5, 0.75, 1]
        for s in solutions:
            for point in points_to_check:
                val = sp.simplify(s.subs(self._y, point).evalf())
                if isinstance(val, sp.core.numbers.Float):
                    val = float(val)
                    if val >= self._low and val <= self._high:
                        return s
        return None


def read_distribution_func() -> str:
    distr_func_str = input("Введите многочлен в формате Python (например, 'x**2 + 2*x - 3'): ")
    return str_to_distribution_func(distr_func_str)


def str_to_distribution_func(distribution_func_str: str):
    try:
        distr_func = sp.sympify(distribution_func_str)
    except sp.SympifyError:
        print("Ошибка: Некорректный ввод многочлена.")
        exit()
    return distr_func


def task1() -> None:
    random.seed(1000)
    x, y = sp.symbols("x y")
    # low = float(input("enter the lowest possible value for the random value: "))
    # high = float(input("enter the highest possible value for the random value: "))
    # if low > high:
    #     print("Incorrect input: low > high")
    #

    low = 0
    high = 2
    distr_func_str = '(1 / 8) * x**2 + x / 4'
    # distr_func_str = 'x**2'
    distr_func = str_to_distribution_func(distr_func_str)
    print("distr_func", distr_func)
    is_correct_distr_func = check_distr_func(distr_func, x, low, high)
    if not is_correct_distr_func:
        print("Incorrect distr func")
        return

    try:
        generator = RVGenerator(distr_func, x, y, low, high)
    except RuntimeError as ex:
        print(ex)
        return

    values = [generator.generate() for _ in range(5000)]

    create_histogram(values, 30)

    statistical_mean = calc_statistical_mean(values)
    practical_dispersion = calc_dispersion(values)
    distr_density = calc_distr_density(distr_func, x)
    print("distr_density: ", distr_density)
    math_expectation = calc_math_expectation(distr_density, x, low, high)
    theoretical_dispersion = calc_theoretical_dispersion(distr_density, x, low, high)

    print("Statistical mean: ", statistical_mean)
    print("Math expectation: ", math_expectation)
    print("Practical dispersion: ", practical_dispersion)
    print("Theoretical dispersion", theoretical_dispersion)

    print(f"Доверительный интервал для мат. ожидания: ", calc_mean_confidence_interval(values, 0.99))
    print(f"Доверительный интервал для среднеквадратичного отклонения: ", calc_standard_deviation_conf_interval(values, 0.99))

    statistical_series = build_statistical_series(values, 100)
    is_true = test_hypothesis(statistical_series, distr_func, x, 0.7)

    if is_true:
        print("Нет оснований отвергать гипотезу о том, что генеральная совокупность распределена по "
              "данному закону распределения.")
    else:
        print("Нет оснований принять гипотезу о том, что генеральная совокупность распределена "
              "по данному закону распределения")
