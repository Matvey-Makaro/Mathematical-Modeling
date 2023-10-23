from statistical_research import create_histogram

from sympy import S
import sympy as sp
from sympy import *
from task1 import task1


def main() -> None:
    task1()

    # # Введите многочлен с консоли
    # # polynomial_str = input("Введите многочлен в формате Python (например, 'x**2 + 2*x - 3'): ")
    # # polynomial_str = 'x**2 - 0.25'
    # polynomial_str = 'x**3 + 10*x - 3'
    # create_histogram([1,1, 2,2, 3, 4], 4)
    #
    # x, y = sp.symbols('x y')
    # try:
    #     polynomial = sp.sympify(polynomial_str)
    # except sp.SympifyError:
    #     print("Ошибка: Некорректный ввод многочлена.")
    #     exit()
    #
    # # Вывод введенного многочлена
    # print("Введенный многочлен:", polynomial)
    #
    # # Задайте функцию распределения (пример: экспоненциальное распределение)
    # # Замените это выражение на свою функцию распределения
    # cdf_expression = polynomial
    #
    # # Найдите обратную функцию
    # inverse_cdf = sp.solve(cdf_expression - y, x)
    # print(inverse_cdf)
    #
    # # equations_and_inequalities = [
    # #     cdf_expression - y,
    # #     x >= 0,
    # #     x <= 1,
    # #     y >= 0,
    # #     y <= 1
    # # ]
    #
    # # Выведите обратную функцию
    # print("Обратная функция распределения:")
    # for eq in inverse_cdf:
    #     print(eq)
    #     val = sp.simplify(eq.subs(y, 0).evalf())
    #     print(type(val))
    #     print(val)

    # x**3 + 10*x - 3
    # x**3 -30*x**2 + 10*x - 3


if __name__ == '__main__':
    main()
