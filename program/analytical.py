import math


# Многоканальное СМО с неограниченной очередью
def phase1() -> None:
    print("######################################")
    print("Phase 1")
    n = 4
    l = 0.75  # человека в минуту
    u = 0.2  # человека в минуту
    load_coeff = l / u  # коэфф. загрузки СМО

    p_0 = 1
    for i in range(1, n):
        p_0 += (load_coeff ** i) / math.factorial(i)
    p_0 += ((load_coeff ** n) / math.factorial(n - 1)) * (1 / (n - load_coeff))
    p_0 = p_0 ** (-1)

    p_queue = ((load_coeff ** n) / math.factorial(n)) * (n / (n - load_coeff)) * p_0

    # TODO: print it
    p_otk = 0
    Q = 1 - p_otk
    A = l * Q

    L_queue = ((load_coeff ** (n + 1)) / math.factorial(n)) * (
            n / ((n - load_coeff) ** 2)) * p_0  # среднее число заявок в очереди
    L_obs = load_coeff  # Среднее число обслуживаемых заявок
    L_smo = L_queue + L_obs  # Среднее число посетителей

    t_smo = L_queue / l + Q / u  # Среднее время, потраченное клиентом

    print("n: ", n)
    print("lambda: ", l)
    print("u: ", u)
    print("load_coeff: ", load_coeff)
    print("p_0:", p_0)
    print("Q: ", Q)
    print("A: ", A)
    print("p_queue:", p_queue)
    print("L_queue: ", L_queue)
    print("L_obs: ", L_obs)
    print("L_smo: ", L_smo)
    print("t_smo: ", t_smo)


# Одноканальное СМО с неограниченной очередью
def phase2() -> None:
    print("######################################")
    print("Phase 2")

    l = 0.75  # человека в минуту
    u = 1  # человека в минуту
    load_coeff = l / u  # коэфф. загрузки СМО

    p_0 = 1 - load_coeff

    # TODO: print it
    p_otk = 0
    Q = 1
    A = l * Q

    L_queue = (load_coeff ** 2) / (1 - load_coeff)  # среднее число заявок в очереди
    L_obs = load_coeff  # Среднее число обслуживаемых заявок
    L_smo = L_queue + L_obs  # Среднее число посетителей

    t_smo = L_smo / l  # Среднее время, потраченное клиентом

    print("lambda: ", l)
    print("u: ", u)
    print("load_coeff: ", load_coeff)
    print("p_0:", p_0)
    print("Q: ", Q)
    print("A: ", A)
    print("L_queue: ", L_queue)
    print("L_obs: ", L_obs)
    print("L_smo: ", L_smo)
    print("t_smo: ", t_smo)


# Многоканальное СМО с неограниченной очередью
def phase3() -> None:
    print("######################################")
    print("Phase 3")
    n = 3
    l = 0.75  # человека в минуту
    u = 1  # человека в минуту
    load_coeff = l / u  # коэфф. загрузки СМО

    p_0 = 1
    for i in range(1, n):
        p_0 += (load_coeff ** i) / math.factorial(i)
    p_0 += ((load_coeff ** n) / math.factorial(n - 1)) * (1 / (n - load_coeff))
    p_0 = p_0 ** (-1)

    p_queue = ((load_coeff ** n) / math.factorial(n)) * (n / (n - load_coeff)) * p_0

    # TODO: print it
    p_otk = 0
    Q = 1 - p_otk
    A = l * Q

    L_queue = ((load_coeff ** (n + 1)) / math.factorial(n)) * (
            n / ((n - load_coeff) ** 2)) * p_0  # среднее число заявок в очереди
    L_obs = load_coeff  # Среднее число обслуживаемых заявок
    L_smo = L_queue + L_obs  # Среднее число посетителей

    t_smo = L_queue / l + Q / u  # Среднее время, потраченное клиентом

    print("n: ", n)
    print("lambda: ", l)
    print("u: ", u)
    print("load_coeff: ", load_coeff)
    print("p_0:", p_0)
    print("Q: ", Q)
    print("A: ", A)
    print("p_queue:", p_queue)
    print("L_queue: ", L_queue)
    print("L_obs: ", L_obs)
    print("L_smo: ", L_smo)
    print("t_smo: ", t_smo)


def analytical_solution() -> None:
    print("analytical_solution:")
    phase1()
    phase2()
    phase3()
