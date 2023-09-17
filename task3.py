from random import random


def simulate_complex_dependent_events(p_a: float, p_b_given_a: float,  num_of_simulations: int = 1) -> list:
    result = []
    p_b_not_given_a = 1 - p_b_given_a

    for _ in range(num_of_simulations):
        x1 = random()
        x2 = random()
        if x1 <= p_a:
            result.append(0 if x2 <= p_b_given_a else 1)
        else:
            result.append(2 if x2 <= p_b_not_given_a else 3)
    return result


def calculate_frequencies(simulations: list) -> list:
    counters = [0 for _ in range(4)]
    for s in simulations:
        counters[s] += 1

    num_of_simulations = len(simulations)
    return [counter / num_of_simulations for counter in counters]


def task3() -> None:
    num_of_simulations = 1000000
    p_a = 0.4
    p_b_given_a = 0.9
    simulations_list = simulate_complex_dependent_events(p_a, p_b_given_a, num_of_simulations)

    print("###########################################################################################################")
    print("Task3")
    print("P(A):", p_a)
    print("P(B|A)", p_b_given_a)
    frequencies = calculate_frequencies(simulations_list)
    print("AB:", frequencies[0])
    print("A!B", frequencies[1])
    print("!AB", frequencies[2])
    print("!A!B", frequencies[3])

    p_b = p_a * p_b_given_a + (1 - p_a) * (1 - p_b_given_a)
    p_a_given_b = p_b_given_a * p_a / p_b
    p_a_given_not_b = (p_a - p_b * p_a_given_b) / (1 - p_b)
    expected_a_b = p_a * p_b_given_a
    expected_a_not_b = (1 - p_b) * p_a_given_not_b
    expected_not_a_b = (1 - p_a) * (1 - p_b_given_a)
    expected_not_a_not_b = 1 - expected_a_b - expected_a_not_b - expected_not_a_b

    print()
    print("expected AB:", expected_a_b)
    print("expected A!B", expected_a_not_b)
    print("expected !AB", expected_not_a_b)
    print("expected !A!B", expected_not_a_not_b)
    print("###########################################################################################################")
