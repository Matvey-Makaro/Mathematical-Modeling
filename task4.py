from random import random


def simulate_full_group_events(probabilities: list, num_of_simulations: int = 1) -> list:
    assert(sum(probabilities) == 1)
    result = []
    for _ in range(num_of_simulations):
        x = random()
        p_sum = 0
        for i in range(len(probabilities)):
            p_sum += probabilities[i]
            if x <= p_sum:
                result.append(i)
                break
    return result


def calculate_frequencies(simulations: list, num_of_events: int) -> list:
    num_of_simulations = len(simulations)
    assert(num_of_simulations != 0)
    counters = [0 for _ in range(num_of_events)]
    for s in simulations:
        counters[s] += 1

    return [counter / num_of_simulations for counter in counters]


def task4() -> None:
    num_of_simulations = 1000000
    probabilities = [0.1, 0.2, 0.4, 0.3]
    simulations_list = simulate_full_group_events(probabilities, num_of_simulations)
    print("###########################################################################################################")
    print("Task4")
    print("Probabilities: ", probabilities)
    frequencies = calculate_frequencies(simulations_list, len(probabilities))
    print("Frequencies: ", frequencies)

    print("###########################################################################################################")