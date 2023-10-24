import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import random
from statistical_research import *
from RVGenerator import *
import matplotlib.pyplot as plt


class ZGenerator:
    def __init__(self, distr_func, x, y, z, low, high):
        self._distr_func = distr_func
        self._x = x
        self._y = y
        self._z = z
        self._inverse_func = None
        self._low = low
        self._high = high

        self._calc_inverse_func()

    def generate(self, z_val: float) -> float:
        uniform_rv = random.uniform(0, 1)
        rv = sp.simplify(self._inverse_func.subs(self._y, uniform_rv).subs(self._z, z_val).evalf())
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
                val = sp.simplify(s.subs(self._y, point).subs(self._z, self._low).evalf())
                if isinstance(val, sp.core.numbers.Float):
                    val = float(val)
                    if val >= self._low and val <= self._high:
                        return s
        return None

def read_distribution_func() -> str:
    distr_func_str = input("Введите многочлен в формате Python (например, 'x**2 + 2*x - 3'): ")
    return str_to_func(distr_func_str)


def str_to_func(func_str: str):
    try:
        distr_func = sp.sympify(func_str)
    except sp.SympifyError:
        print("Ошибка: Некорректный ввод многочлена.")
        exit()
    return distr_func


def create_plot_2d(f_x, x, x_values):
    vals = np.linspace(0, 1, 100)
    f_x_values = [float(f_x.subs(x, v).evalf()) for v in vals]
    plt.plot(vals, f_x_values, color='red')
    plt.hist(x_values, 30, color='blue', density=1)
    plt.show()


def get_rv_generator(F, var, low, high) -> RVGenerator:
    y = sp.symbols("y")
    is_correct_distr_func = check_distr_func(F, var, low, high)
    if not is_correct_distr_func:
        print("Incorrect distr func")
        return

    try:
        generator = RVGenerator(F, var, y, low, high)
    except RuntimeError as ex:
        print(ex)
        return
    return generator


def task1() -> None:
    # random.seed(1000)
    x, y, z = sp.symbols("x y z")

    low = 0
    high = 1
    distr_density_str = '2*(x**2 + z/3)'

    f_x_z = str_to_func(distr_density_str)
    f_x = sp.integrate(f_x_z, (z, 0, 1))
    f_z = sp.integrate(f_x_z, (x, 0, 1))
    f_x_if_z = sp.simplify(f_x_z / f_z)
    f_z_if_x = sp.simplify(f_x_z / f_x)

    F_x = sp.integrate(f_x, (x, 0, x))
    F_z = sp.integrate(f_z, (z, 0, z))
    F_z_if_x = sp.integrate(f_z_if_x, (z, 0, z))

    print("f(x):", f_x)
    print("f(z): ", f_z)
    print("f(x|z):", f_x_if_z)
    print("f(z|x):", f_z_if_x)
    print("F(x): ", F_x)
    print("F(z):", F_z)
    print("F(z|x):", F_z_if_x)

    if f_x != f_x_if_z:
        print("Составляющие двумерной НСВ зависимы т.к. f(x) != f(x|z)")
    else:
        print("Составляющие двумерной НСВ независимы т.к. f(x) = f(x|z)")

    M_x = calc_math_expectation(f_x, x, low, high)
    M_z = calc_math_expectation(f_z, z, low, high)
    print("M(x) = ", M_x)
    print("M(z) = ", M_z)

    D_x = calc_theoretical_dispersion(f_x, x, low, high)
    D_z = calc_theoretical_dispersion(f_z, z, low, high)
    print("D(x) = ", D_x)
    print("D(z) = ", D_z)

    r = calc_theor_correlation(f_x_z, f_x, x, low, high, f_z, z, low, high)
    print("r: ", r)

    num_of_vals_to_generate = 2000
    x_generator = get_rv_generator(F_x, x, low, high)
    x_values = [x_generator.generate() for _ in range(num_of_vals_to_generate)]

    z_values = []
    z_generator = ZGenerator(F_z_if_x, z, y, x, low, high)
    for x in x_values:
        z_values.append(z_generator.generate(x))

    x, y, z = sp.symbols("x y z")

    stat_M_x = calc_statistical_mean(x_values)
    stat_M_z = calc_statistical_mean(z_values)
    print("stat_M_x:", stat_M_x)
    print("stat_M_z:", stat_M_z)


    stat_D_x = calc_dispersion(x_values)
    stat_D_z = calc_dispersion(z_values)
    print("stat_D_x:", stat_D_x)
    print("stat_D_z:", stat_D_z)

    stat_r = calc_correlation(x_values, z_values)
    print("stat_r: ", stat_r)

    create_plot_2d(f_x, x, x_values)
    create_plot_2d(f_z, z, z_values)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    hist, _, _ = np.histogram2d(x_values, z_values, bins=[10, 10])
    ax.hist(hist)
    fig.show()
    plt.show()
