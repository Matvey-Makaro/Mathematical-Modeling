import sympy as sp
import random


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
