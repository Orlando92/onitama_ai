import random
import copy

from game.dicts import CARD_DEFINITIONS
from game.card import Card
from game.game_state import GameState
from game.utils import GameUtils

class Game:
    def __init__(self, players, wait_for_input):
        self.game_state_history = []
        self.wait_for_input = wait_for_input
        self.players = players 
        board = self.setup_pieces()
        player_one_cards, player_two_cards, neutral_card = self.deal_cards()
        starting_player_index = 0 if neutral_card.color == "red" else 1
        self.game_state = GameState(board, player_one_cards, player_two_cards, neutral_card, starting_player_index)
        self.stats = None

    def setup_pieces(self):
        board = []
        for x in range(5):
            row = []
            for y in range(5):
                if x == 0 or x == 4:
                    if y != 2:
                        row.append(("P", x//4))
                    else:
                        row.append(("M", x//4))
                else:
                    row.append(None)
            board.append(row)
        return board

    def deal_cards(self):
        all_cards = self.load_all_cards()
        selected = random.sample(all_cards, 5)
        return selected[:2], selected[2:4], selected[4]

    def start(self):
        self.stats = {
            0: [], 
            1: []
        }

        winner = None
        while winner == None:
            player = self.players[self.game_state.current_player_index]
            print(f"Current player: {player.name} (Player {self.game_state.current_player_index})")
            print(f"Current hand: {[card.name for card in self.game_state.cards[player.index]]}")
            move, stats = player.choose_move(self.game_state)
            self.stats[player.index].append(stats)
            self.apply_move(move)
            GameUtils.draw_board(self.game_state.board)
            winner = GameUtils.get_winner(self.game_state, print_winner=True)
            if (self.wait_for_input):
                input("Press Enter to continue...")

        average_stats = self.average_stats()

        return winner, average_stats

    
        

    def apply_move(self, move):
        self.game_state_history.append(self.game_state)
        self.game_state = GameUtils.apply_move(self.game_state, move) 


    def load_all_cards(self):
        return [Card(name, info['moves'], info['color']) for name, info in CARD_DEFINITIONS.items()]

    def average_stats(self):
        average_stats = {}
        for player_index in self.stats:

            if len(self.stats[player_index]) == 0:
                average_stats[player_index] = {
                    'nodes_evaluated': 0,
                    'time_taken': 0
                }
                continue

            total_nodes_evaluated = sum(stat['nodes_evaluated'] for stat in self.stats[player_index])
            total_time_taken = sum(stat['time_taken'] for stat in self.stats[player_index])
            average_stats[player_index] = {
                'nodes_evaluated': total_nodes_evaluated / len(self.stats[player_index]),
                'time_taken': total_time_taken / len(self.stats[player_index]) 
            }
        return average_stats
    
