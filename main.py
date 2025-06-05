import yaml
from ai.strategy_factory import StrategyFactory
from game.game import Game
from game.player import Player


config = yaml.safe_load(open("properties.yml"))

print(f"config: {config}")

def main():
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

    game = Game([player_one, player_two], config['wait_for_input'])
    game.start()


if __name__ == "__main__":
    main()
