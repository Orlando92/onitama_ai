class GameState:
    def __init__(self, board, player_one_cards, player_two_cards, neutral_card, current_player_index,):
        self.board = board
        self.cards = {
            0: player_one_cards,
            1: player_two_cards
        }
        self.neutral_card = neutral_card 
        self.current_player_index = current_player_index


