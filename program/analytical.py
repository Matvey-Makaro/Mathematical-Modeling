import math


class Stat:
    def __init__(self):
        self.n = None
        self.l = None
        self.u = None
        self.load_coeff = None
        self.p_0 = None
        self.Q = None
        self.A = None
        self.p_queue = None
        self.L_queue = None
        self.L_obs = None
        self.L_smo = None
        self.t_smo = None


def print_stat(stat: Stat) -> None:
    if stat.n is not None:
        print("Число каналов(n): ", stat.n)
    if stat.l is not None:
        print("Интенсивность поступления заявок(lambda): ", stat.l)
    if stat.u is not None:
        print("Интенсивность обслуживания заявок(nu): ", stat.u)
    if stat.load_coeff is not None:
        print("Коэффициент загрузки(load_coeff): ", stat.load_coeff)
    if stat.p_0 is not None:
        print("p_0:", stat.p_0)
    if stat.Q is not None:
        print("Относительная пропускная способность(Q): ", stat.Q)
    if stat.A is not None:
        print("Абсолютная пропускная способность(A): ", stat.A)
    if stat.p_queue is not None:
        print("Вероятность образования очереди(p_queue):", stat.p_queue)
    if stat.L_queue is not None:
        print("Среднее число посетителей в очереди(L_queue): ", stat.L_queue)
    if stat.L_obs is not None:
        print("Среднее число обслуживаемых посетителей(L_obs): ", stat.L_obs)
    if stat.L_smo is not None:
        print("Среднее число посетителей(L_smo): ", stat.L_smo)
    if stat.t_smo is not None:
        print("Среднее время, затрачиваемое посетителем(t_smo): ", stat.t_smo)


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

    stat = Stat()
    stat.n = n
    stat.l = l
    stat.u = u
    stat.load_coeff = load_coeff
    stat.p_0 = p_0
    stat.Q = Q
    stat.A = A
    stat.p_queue = p_queue
    stat.L_queue = L_queue
    stat.L_obs = L_obs
    stat.L_smo = L_smo
    stat.t_smo = t_smo
    print_stat(stat)


# Одноканальное СМО с неограниченной очередью
def phase2() -> None:
    print("######################################")
    print("Phase 2")

    n = 1
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

    stat = Stat()
    stat.n = n
    stat.l = l
    stat.u = u
    stat.load_coeff = load_coeff
    stat.p_0 = p_0
    stat.Q = Q
    stat.A = A
    stat.L_queue = L_queue
    stat.L_obs = L_obs
    stat.L_smo = L_smo
    stat.t_smo = t_smo
    print_stat(stat)


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

    stat = Stat()
    stat.n = n
    stat.l = l
    stat.u = u
    stat.load_coeff = load_coeff
    stat.p_0 = p_0
    stat.Q = Q
    stat.A = A
    stat.p_queue = p_queue
    stat.L_queue = L_queue
    stat.L_obs = L_obs
    stat.L_smo = L_smo
    stat.t_smo = t_smo
    print_stat(stat)


def analytical_solution() -> None:
    print("analytical_solution:")
    phase1()
    phase2()
    phase3()
