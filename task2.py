from random import random
from task1 import simulate_simple_rand_events


def calculate_frequencies(simulations: list) -> list:
    num_of_simulations = len(simulations)
    if num_of_simulations == 0:
        return []

    num_of_events = len(simulations[0])
    counters = [0 for i in range(num_of_events)]
    for simulation in simulations:
        assert len(simulation) == len(counters)
        for i in range(len(simulation)):
            if simulation[i] == 1:
                counters[i] += 1

    counters = [counter / num_of_simulations for counter in counters]
    return counters


def simulate_complex_rand_events(probabilities: list, num_of_simulations: int = 1) -> list:
    result = [[] for i in range(num_of_simulations)]
    for p in probabilities:
        events = simulate_simple_rand_events(p, num_of_simulations)
        for i in range(num_of_simulations):
            result[i].append(events[i])
    return result


def task2() -> None:
    num_of_simulations = 1000000
    probabilities = [0.3, 0.45, 0.9]
    simulations_list = simulate_complex_rand_events(probabilities, num_of_simulations)

    print("###########################################################################################################")
    print("Task2")
    print("P:", probabilities)
    print("Calculated frequency: ", calculate_frequencies(simulations_list))
    print("###########################################################################################################")
