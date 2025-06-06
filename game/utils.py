import copy

from game.game_state import GameState
from game.move import Move 

class GameUtils:
    @staticmethod
    def get_winner(state, print_winner=False):
        board = state.board
        p1_master_alive = False
        p2_master_alive = False
        p1_master_pos = None
        p2_master_pos = None

        current_player_index = state.current_player_index

        legal_moves = GameUtils.get_legal_moves(state)

        if (len(legal_moves) == 0): 
            if print_winner:
                print(f"Player {current_player_index} has no legal moves left! Player {1 - current_player_index} wins!")
            return 1 - current_player_index


         

        for x in range(5):
            for y in range(5):
                cell = board[x][y]
                if cell == ('M', 0):
                    p1_master_alive = True
                    p1_master_pos = (x, y)
                elif cell == ('M', 1):
                    p2_master_alive = True
                    p2_master_pos = (x, y)

        if not p2_master_alive:
            if print_winner:
                print("Player 1 Master got killed! Player 0 wins!")
            return 0
        if not p1_master_alive:
            if print_winner:
                print("Player 0 Master got killed! Player 1 wins!")
            return 1
        if p1_master_pos == (4, 2):
            if print_winner:
                print("Player 0 Master reached the goal! Player 0 wins!")
            return 0
        if p2_master_pos == (0, 2):
            if print_winner:
                print("Player 1 Master reached the goal! Player 1 wins!")
            return 1
        return None


    @staticmethod
    def update_board(board, move):
        x1, y1 = move.from_position
        x2, y2 = move.to_position

        new_board = []
        for x in range(5):
            row = []
            for y in range(5):
                if x == x1 and y == y1:
                    row.append(None)
                elif x == x2 and y == y2:
                    row.append(board[x1][y1])
                else:
                    row.append(board[x][y])
            new_board.append(row)

        return new_board


    @staticmethod
    def draw_board(board):
        print("Current board state:")
        for row in board:
            print(" | ".join(f"{cell[0]}{cell[1]}" if cell else "--" for cell in row))
        print("\n")

    @staticmethod
    def apply_move(state, move):
        board = GameUtils.update_board(state.board, move)
        player_index = state.current_player_index
        other_index = 1 - player_index
        card_used = move.card

        hand = list(state.cards[player_index])
        other_hand = list(state.cards[other_index])
        used_card = next(card for card in hand if card.name == card_used.name)

        hand.remove(used_card)
        hand.append(state.neutral_card)

        if player_index == 0:
            cards_p1 = hand
            cards_p2 = other_hand
        else:
            cards_p1 = other_hand
            cards_p2 = hand

        return GameState(
            board, 
            cards_p1,
            cards_p2,
            used_card,
            other_index 
        )

    @staticmethod
    def get_legal_moves(state):
        # print("Calculating legal moves...")
        legal_moves = []
        board = state.board
        player_index = state.current_player_index
        hand = state.cards[player_index]
        # print(f"Player {player_index} has cards: {[card.name for card in hand]}")
        for card in hand:
            for x in range(5):
                for y in range(5):
                    if board[x][y] is not None and board[x][y][1] == player_index:
                        for (dx, dy) in card.moves:
                            new_x = x + (dx if player_index == 0 else -dx)
                            new_y = y + (dy if player_index == 0 else -dy)
                            if 0 <= new_x < 5 and 0 <= new_y < 5:
                                if board[new_x][new_y] is None or board[new_x][new_y][1] != player_index:
                                    legal_moves.append(Move(
                                        card,
                                        (x, y),
                                        (new_x, new_y),
                                    ))

        return legal_moves


        
