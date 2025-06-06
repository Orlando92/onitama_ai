import yaml
from ai.strategy_factory import StrategyFactory
from game.game import Game
from game.player import Player


config = yaml.safe_load(open("properties.yml"))

simulations = config.get('simulations', 1)


print(f"config: {config}")

results = []

def main():


    csv_rows = [
      [
        'winner',
        'player_0_time'
        'player_1_time',
        'player_0_nodes_evaluated',
        'player_1_nodes_evaluated',
      ]
    ]

    player_one_wins = 0
    player_two_wins = 0
    player_one_strategy_chosen = config['player_one']['strategy']
    player_two_strategy_chosen = config['player_two']['strategy']
    player_one_minimax_params = config['player_one']['minimax']
    player_two_minimax_params = config['player_two']['minimax']
    
    player_one_strategy = StrategyFactory.create_strategy(player_one_strategy_chosen)
    if player_one_strategy_chosen == "minimax":
        player_one_strategy.set_params(player_one_minimax_params)
    player_two_strategy = StrategyFactory.create_strategy(player_two_strategy_chosen)
    if player_two_strategy_chosen == "minimax":
        player_two_strategy.set_params(player_two_minimax_params)

    
    player_one = Player(0, config['player_one']['name'], player_one_strategy)
    player_two = Player(1, config['player_two']['name'], player_two_strategy)

    for _ in range(simulations):
        game = Game([player_one, player_two], config['wait_for_input'])
        winner, average_stats = game.start()
        if winner == 0:
            player_one_wins += 1
        else:
            player_two_wins += 1

        csv_rows.append([
            winner,
            average_stats[0]['time_taken'],
            average_stats[1]['time_taken'],
            average_stats[0]['nodes_evaluated'],
            average_stats[1]['nodes_evaluated'],
        ])

    print(f"Player 0 ({player_one.name}) wins: {player_one_wins} times")
    print(f"Player 1 ({player_two.name}) wins: {player_two_wins} times")
    
    
    with open(f"output.csv", "w") as file:
      file.write('\n'.join([','.join([str(val) for val in row]) for row in csv_rows]))


        

    
        


if __name__ == "__main__":
    main()
