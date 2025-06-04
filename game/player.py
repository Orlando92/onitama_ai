class Player:
    def __init__(self, index, name, strategy):
        self.index = index
        self.name = name
        self.strategy = strategy

    def choose_move(self, game_state):
        return self.strategy.choose_move(game_state, self.index)

