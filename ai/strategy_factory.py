from ai.minimax import Minimax 

class StrategyFactory: 

    @staticmethod
    def create_strategy(strategy_name: str):
        if strategy_name == "minimax":
            return Minimax()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

