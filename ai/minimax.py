import time

from ai.strategy import Strategy
from game.utils import GameUtils
from game.dicts import MASTER_GOAL


class Minimax(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "Minimax Strategy"
        self.stats = {
            'nodes_evaluated': 0,
            'time_taken': 0,
        }

    def choose_move(self, state, player_index, depth=None):

        self.stats['nodes_evaluated'] = 0  # Reset the nodes evaluated counter
        start_time = time.time()

        if depth is None:
            depth = self.params.get('depth', 3)
        # print(f"Choosing move for player {player_index} with depth {depth}")
        best_move = None
        best_score = float('-inf')
        for move in GameUtils.get_legal_moves(state):
            # print(f"Evaluating move: {move.card.name} from {move.from_position} to {move.to_position}")
            new_state = GameUtils.apply_move(state, move)
            # print(f"New state after move: {new_state.__dict__}")
            score = self.min_value(new_state, depth - 1, player_index)
            # print(f"Score for move {move.card.name} from {move.from_position} to {move.to_position}: {score}")
            if score > best_score:
                best_score = score
                best_move = move
        print(f"Best move chosen by Minimax: {best_move.card.name} from {best_move.from_position} to {best_move.to_position} with score {best_score}")
        end_time = time.time()
        self.stats['time_taken'] = end_time - start_time
        return best_move, self.stats

    def min_value(self, state, depth, root_player_index):

        self.stats["nodes_evaluated"] += 1  # Incrementa el contador de nodos evaluados
        # print(f"Min value called with depth {depth} for player {state.current_player_index}")
        winner = GameUtils.get_winner(state)
        if depth == 0 or winner is not None:
            return self.evaluate_state(state, root_player_index)

        player_index = state.current_player_index

        v = float('inf')
        for move in GameUtils.get_legal_moves(state):
            new_state = GameUtils.apply_move(state, move)
            v = min(v, self.max_value(new_state, depth - 1, root_player_index))
        return v

    def max_value(self, state, depth, root_player_index):
        self.stats["nodes_evaluated"] += 1  # Incrementa el contador de nodos evaluados
        # print(f"Max value called with depth {depth} for player {state.current_player_index}")
        winner = GameUtils.get_winner(state)
        if depth == 0 or winner is not None:
            return self.evaluate_state(state, root_player_index)

        player_index = state.current_player_index

        v = float('-inf')
        for move in GameUtils.get_legal_moves(state):
            new_state = GameUtils.apply_move(state, move)
            v = max(v, self.min_value(new_state, depth - 1, root_player_index))
        return v

    
    def evaluate_state(self, state, player_index):
        params = self.params
        win = params.get('win', 1000)
        board = state.board

        enemy_index = 1 - player_index

        if(winner := GameUtils.get_winner(state)) is not None:
            return win if winner == player_index else -1 * win
        score = 0

        student_alive = params.get('student_alive', 10)
        master_alive = params.get('master_alive', 100)
        student_threaten = params.get('student_threaten', 5)
        master_threaten = params.get('master_threaten', 50)
        master_distance_goal = params.get('master_distance_goal', 5)
        
        for x in range(5):
            for y in range(5):
                cell = board[x][y]
                if cell is None:
                    continue
                piece, player_piece = cell
                if piece == 'M':
                    score += master_alive if player_piece == player_index else -master_alive
                    master_goal = MASTER_GOAL[player_piece]
                    score += master_distance_goal * (abs(master_goal[0] - x) + abs(master_goal[1] - y)) * (1 if player_piece == player_index else -1)
                    

                elif piece == 'S':
                    score += student_alive if player_piece == player_index else -student_alive
                


                for player_index_cards in state.cards:
                    for card in state.cards[player_index_cards]:
                        if (player_index_cards == player_piece):
                            for move in card.moves:
                                (dx, dy) = move
                                nx, ny = x + (dx if player_index_cards == 0 else -dx), y + (dy if player_index_cards == 0 else -dy)
                                if 0 <= nx < 5 and 0 <= ny < 5:
                                    if board[nx][ny] is not None and board[nx][ny][1] == (1 - player_index_cards):
                                        if board[nx][ny][0] == 'M':
                                            score += -master_threaten if player_index_cards == player_index else master_threaten
                                        else:
                                            score += -student_threaten if player_index_cards == player_index else student_threaten



        return score
