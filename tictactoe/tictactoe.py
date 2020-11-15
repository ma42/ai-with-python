"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

test_board = [[X, O, EMPTY],
             [O, X, O],
             [X, X, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = [state for row in board for state in row]
    X_count = flat_board.count(X)
    O_count = flat_board.count(O)

    if len(set(flat_board)) <= 1 or X_count <= O_count:
        return X
    else: 
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    res_board = copy.deepcopy(board)
    if action in actions(res_board):
        res_board[action[0]][action[1]] = player(res_board)
    else:
        raise ValueError
    return res_board

def check_row(board):
    """
    Returns boolean and winning player, if the board contains a row with a winner. 
    """
    for row in board:
        if len(set(row)) == 1:
            return True, row[0] 
    else:
        return False, None

def check_diagonal(board):
    """
    Returns boolean and winning player, if the board contains a diagonal with a winner. 
    """
    diag1 = set([board[i][i] for i in range(3)])
    diag2 = set([board[i][len(board)-i-1] for i in range(3)])
    if len(diag1) == 1:
        return True, board[0][0]
    elif len(diag2) == 1:
        return True, board[0][2]
    else:
        return False, None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_row = check_row(board)
    winner_diag = check_diagonal(board)
    winner_col = check_row(np.transpose(board))

    if winner_row[0]:
        return winner_row[1]
    elif winner_diag[0]:
        return winner_diag[1]
    elif  winner_col[0]:
        return winner_col[1]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not actions(board) or not winner(board) == None:
        return True
    else: 
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        return 0, 1
        
    current_player = player(board)
    current_value = float("-inf") if current_player == X else float("inf")

    for move in actions(board):
        new_value = recursive_minimax(result(board, move), current_value)
        new_value = max(current_value, new_value) if current_player == X else min(current_value, new_value)
        if new_value != current_value:
            current_value = new_value
            best_move = move
    
    return best_move

def recursive_minimax(board, best_value):
    if terminal(board):
        return utility(board)

    current_player = player(board)
    value = float("-inf") if current_player == X else float("inf")
    for move in actions(board):
        new_value = recursive_minimax(result(board, move), value)
        
        if current_player == X:
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)
    return value