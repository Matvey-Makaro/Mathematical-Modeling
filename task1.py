from random import random


def simulate_simple_rand_events(p: float, num_of_simulations: int = 1) -> list:
    return [int(random() <= p) for i in range(num_of_simulations)]


def calc_frequency(simulations: list) -> float:
    counter = 0
    for s in simulations:
        if s == 1:
            counter += 1
    return counter / len(simulations)


def save_simulation(simulation: list, fname: str):
    with open(fname, "w") as f:
        for i in simulation:
            f.write(str(i) + '\n')


def load_simulation(fname: str) -> list:
    result = []
    with open(fname, "r") as f:
        lines = f.readlines()
        return [int(l) for l in lines]


def task1() -> None:
    num_of_simulations = 1000000
    fname = "Task1"
    P = 0.1
    simulations_list = simulate_simple_rand_events(P, num_of_simulations)
    # print("simulations_list befor save: ", simulations_list)
    # save_simulation(simulations_list, fname)
    # loaded_list = load_simulation(fname)
    # print("loaded_list:", loaded_list)

    print("###########################################################################################################")
    print("Task1")
    print("P:", P)
    print("Calculated frequency: ", calc_frequency(simulations_list))
    print("###########################################################################################################")
