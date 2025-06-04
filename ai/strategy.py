class Strategy: 
    def __init__(self):
        self.name = "Default Strategy"
        self.params = None

    def choose_move(self, game_state):
        return None

    def set_params(self, params):
        print(f"Setting parameters for {self.name} strategy: {params}")
        self.params = params

