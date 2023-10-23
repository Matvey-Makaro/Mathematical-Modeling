import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import random
from statistical_research import *
from RVGenerator import *
import matplotlib.pyplot as plt


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


def create_plot_2d(f_x, f_z, x, z, x_values, z_values):
    vals = np.linspace(0, 1, 100)
    # f_x_values = [f_x.subs(x, v).evalf() for v in vals]
    f_z_values = [f_z.subs(z, v).evalf() for v in vals]

    # plt.plot(vals, f_x_values, color='red')
    plt.plot(vals, f_z_values, color='green')
    # plt.hist(x_values, 30, color='blue', density=1)
    plt.hist(z_values, 30, color='black', density=1)

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
    random.seed(1000)
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

    print("f(x):", f_x)
    print("f(z): ", f_z)
    print("f(x|z):", f_x_if_z)
    print("f(z|x):", f_z_if_x)
    print("F(x): ", F_x)
    print("F(z):", F_z)

    if f_x != f_x_if_z:
        print("Составляющие двумерной ДСВ зависимы т.к. f(x) != f(x|z)")
    else:
        print("Составляющие двумерной ДСВ независимы т.к. f(x) = f(x|z)")

    M_x = calc_math_expectation(f_x, x, low, high)
    M_z = calc_math_expectation(f_z, z, low, high)
    print("M(x) = ", M_x)
    print("M(z) = ", M_z)

    D_x = calc_theoretical_dispersion(f_x, x, low, high)
    D_z = calc_theoretical_dispersion(f_z, z, low, high)
    print("D(x) = ", D_x)
    print("D(z) = ", D_z)

    r = calc_theor_correlation(f_x, x, low, high, f_z, z, low, high)
    print("r: ", r)

    num_of_vals_to_generate = 5000
    x_generator = get_rv_generator(F_x, x, low, high)
    x_values = [x_generator.generate() for _ in range(num_of_vals_to_generate)]
    z_generator = get_rv_generator(F_z, z, low, high)
    z_values = [z_generator.generate() for _ in range(num_of_vals_to_generate)]

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

    create_plot_2d(f_x, f_z, x, z, x_values, z_values)

    # x = np.linspace(0, 1, 100)
    # y = np.sin(x)
    # plt.plot(x, y)
    # plt.show()
    # create_histogram(x_values, 30)

    statistical_mean = calc_statistical_mean(x_values)
    practical_dispersion = calc_dispersion(x_values)
    distr_density = calc_distr_density(distr_func, x)
    print("distr_density: ", distr_density)
    math_expectation = calc_math_expectation(distr_density, x, low, high)
    theoretical_dispersion = calc_theoretical_dispersion(distr_density, x, low, high)

    print("Statistical mean: ", statistical_mean)
    print("Math expectation: ", math_expectation)
    print("Practical dispersion: ", practical_dispersion)
    print("Theoretical dispersion", theoretical_dispersion)

    print(f"Доверительный интервал для мат. ожидания: ", calc_mean_confidence_interval(x_values, 0.99))
    print(f"Доверительный интервал для среднеквадратичного отклонения: ",
          calc_standard_deviation_conf_interval(x_values, 0.99))

    statistical_series = build_statistical_series(x_values, 500)
    is_true = test_hypothesis(statistical_series, distr_func, x, 0.7)

    if is_true:
        print("Нет оснований отвергать гипотезу о том, что генеральная совокупность распределена по "
              "данному закону распределения.")
    else:
        print("Нет оснований принять гипотезу о том, что генеральная совокупность распределена "
              "по данному закону распределения")
