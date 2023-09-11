import random
from task4 import simulate_full_group_events


def fortune_wheel(game_to_money_amount: dict) -> str:
    total_money_amount = sum(game_to_money_amount.values())
    games = list(game_to_money_amount.keys())
    probabilities = [money_amount / total_money_amount for money_amount in game_to_money_amount.values()]
    index = simulate_full_group_events(probabilities)[0]
    return games[index]


def read_game_to_money_amount(fname: str) -> dict:
    game_to_money_amount = {}
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            index = line.rfind(" ")
            game = line[0:index:1]
            money_amount = int(line[index + 1::])
            game_to_money_amount[game] = game_to_money_amount.get(game, 0) + money_amount
    return game_to_money_amount


def generate_fortune_wheel_data(fname: str, games: list, num_of_donates: int, max_sum: int = 1000) -> None:
    with open(fname, "w") as f:
        for _ in range(num_of_donates):
            f.write(games[random.randint(0, len(games) - 1)] + " ")
            money_amount = random.randint(1, max_sum)
            f.write(str(money_amount) + "\n")


def calc_game_probability(game_to_money_amount: dict) -> dict:
    games = list(game_to_money_amount.keys())
    total_money_amount = sum(game_to_money_amount.values())
    probabilities = [money_amount / total_money_amount for money_amount in game_to_money_amount.values()]
    assert (sum(probabilities) == 1)
    return dict(zip(games, probabilities))


def fortune_wheel_task() -> None:
    games = ["The Elder Scrolls 5",
             "Grand Theft Auto 5",
             "Minecraft",
             "Grand Theft Auto: San Andreas",
             "Assassin's Creed 2",
             "Mafia 2",
             "Far Cry 3",
             "Need for Speed: Most Wanted",
             "Battlefield 3",
             "The Witcher 3: Wild Hunt"]
    fname = "fortune_wheel_data.txt"
    # generate_fortune_wheel_data(fname, games, num_of_donates=10)

    game_to_money_amount = read_game_to_money_amount(fname)

    print("###########################################################################################################")
    print("Fortune wheel task")
    print("Games and probabilities: ")
    print(calc_game_probability(game_to_money_amount))

    selected_games = []
    for _ in range(1000000):
        selected_games.append(fortune_wheel(game_to_money_amount))

    print("Games and frequencies")
    for game in games:
        count = selected_games.count(game)
        frequency = count / len(selected_games)
        print(game, ": ", frequency)
    print("###########################################################################################################")
