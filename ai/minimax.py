
from ai.strategy import Strategy
from game.utils import GameUtils

class Minimax(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "Minimax Strategy"

    def choose_move(self, state, player_index, depth=None):
        if depth is None:
            depth = self.params.get('depth', 3)
        best_move = None
        best_score = float('-inf')
        for move in GameUtils.get_legal_moves(state):
            new_state = GameUtils.apply_move(state, move)
            score = self.min_value(new_state, depth - 1, player_index)
            if score > best_score:
                best_score = score
                best_move = move
        print(f"Best move chosen by Minimax: {best_move.card.name} from {best_move.from_position} to {best_move.to_position} with score {best_score}")
        return best_move

    def min_value(self, state, depth, root_player_index):
        winner = GameUtils.get_winner(state.board)
        if depth == 0 or winner is not None:
            return self.evaluate_board(state.board, root_player_index)

        player_index = state.current_player_index

        v = float('inf')
        for move in GameUtils.get_legal_moves(state):
            new_state = GameUtils.apply_move(state, move)
            v = min(v, self.max_value(new_state, depth - 1, root_player_index))
        return v

    def max_value(self, state, depth, root_player_index):
        winner = GameUtils.get_winner(state.board)
        if depth == 0 or winner is not None:
            return self.evaluate_board(state.board, root_player_index)

        player_index = state.current_player_index

        v = float('-inf')
        for move in GameUtils.get_legal_moves(state):
            new_state = GameUtils.apply_move(state, move)
            v = max(v, self.min_value(new_state, depth - 1, root_player_index))
        return v

    
    def evaluate_board(self, board, player_index):
        params = self.params
        win = params.get('win', 1000)

        if(winner := GameUtils.get_winner(board)) is not None:
            return win if winner == player_index else -1 * win
        score = 0

        student_alive = params.get('student_alive', 10)
        master_alive = params.get('master_alive', 100)
        
        for x in range(5):
            for y in range(5):
                cell = board[x][y]
                if cell is None:
                    continue
                piece, player = cell
                if piece == 'M':
                    score += master_alive if player == player_index else -master_alive
                elif piece == 'S':
                    score += student_alive if player == player_index else -student_alive
        return score
