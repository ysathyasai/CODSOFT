from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# The game board, represented as a list of 9 strings.
# Each element can be '', 'X', or 'O'.
board = ['' for _ in range(9)]
# Global variables to store the symbols for the human player and the AI.
# These are initialized with defaults but can be changed by the player.
HUMAN = 'X'  # Default human player symbol
AI = 'O'     # Default AI player symbol

def check_winner(board):
    """
    Checks the current state of the board to determine if there's a winner or a tie.
    
    Args:
        board (list): The current 9-element list representing the Tic-Tac-Toe board.
        
    Returns:
        str: 'X' if human wins, 'O' if AI wins, 'tie' if the board is full with no winner,
             or None if the game is still ongoing.
    """
    # Define all possible winning combinations (rows, columns, and diagonals).
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    # Iterate through each winning line to check if any player has won.
    # A player wins if all three positions in a line are occupied by their symbol
    # and that symbol is not empty.

    
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != '':
            return board[line[0]]
    
    if '' not in board:
        return 'tie'
    return None

def get_available_moves(board):
    """Return list of empty positions on the board"""
    return [i for i, spot in enumerate(board) if spot == '']

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Implements the Minimax algorithm with Alpha-Beta pruning to find the optimal move.
    This function recursively evaluates all possible game states.

    Args:
        board (list): The current state of the Tic-Tac-Toe board.
        depth (int): The current depth in the game tree (number of moves made).
        is_maximizing (bool): True if it's the AI's turn (maximizing player), False if it's the human's turn (minimizing player).
        alpha (float): The best score that the maximizer currently can guarantee at this level or above.
        beta (float): The best score that the minimizer currently can guarantee at this level or above.

    Returns:
        int: The score of the current board state from the perspective of the AI.
             (1 for AI win, -1 for human win, 0 for tie).
    """
    # Check for terminal states (win, lose, or tie) to determine the score.
    result = check_winner(board)
    
    # Base cases: If the game has ended, return the corresponding score.
    if result == AI:
        return 1  # AI wins, return a positive score
    elif result == HUMAN:
        return -1 # Human wins, return a negative score
    elif result == 'tie':
        return 0  # It's a tie, return a neutral score
        
    # If it's the AI's turn (maximizing player).
    if is_maximizing:
        best_score = -math.inf # Initialize best_score to negative infinity
        # Iterate through all available moves.
        for move in get_available_moves(board):
            board[move] = AI # Make the move for the AI
            # Recursively call minimax for the next turn (minimizing player).
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = ''   # Undo the move (backtrack) for exploring other branches
            best_score = max(score, best_score) # Update best_score with the maximum score found
            alpha = max(alpha, best_score)       # Update alpha (maximizer's best option)
            # Alpha-Beta Pruning: If beta is less than or equal to alpha, 
            # it means the current branch won't be chosen by the minimizing player,
            # so we can stop exploring this branch.
            if beta <= alpha:
                break
        return best_score
    # If it's the human's turn (minimizing player).
    else:
        best_score = math.inf  # Initialize best_score to positive infinity
        # Iterate through all available moves.
        for move in get_available_moves(board):
            board[move] = HUMAN # Make the move for the human
            # Recursively call minimax for the next turn (maximizing player).
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move] = ''    # Undo the move (backtrack)
            best_score = min(score, best_score) # Update best_score with the minimum score found
            beta = min(beta, best_score)        # Update beta (minimizer's best option)
            # Alpha-Beta Pruning: If beta is less than or equal to alpha, 
            # it means the current branch won't be chosen by the maximizing player,
            # so we can stop exploring this branch.
            if beta <= alpha:
                break
        return best_score

def get_best_move(board):
    """
    Determines the best possible move for the AI player using the minimax algorithm.
    It iterates through all available moves, simulates each move, and evaluates it
    using the minimax function to find the move that yields the highest score for the AI.

    Args:
        board (list): The current state of the Tic-Tac-Toe board.

    Returns:
        int: The index of the best move for the AI.
    """
    best_score = -math.inf # Initialize best_score to negative infinity to ensure any valid score is greater.
    best_move = None       # Initialize best_move to None.
    
    # Iterate over all empty spots on the board.
    for move in get_available_moves(board):
        board[move] = AI # Simulate making the AI's move.
        # Call minimax to evaluate this move. We assume the human will play optimally (minimizing).
        # The depth is 0 as this is the initial call for a potential move.
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = ''   # Undo the move to restore the board to its original state for the next iteration.
        
        # If the score from this move is better than the current best_score, update best_score and best_move.
        if score > best_score:
            best_score = score
            best_move = move
            
    return best_move

@app.route('/')
def home():
    """
    Renders the main game page.
    This is the entry point for the web application.
    """
    return render_template('index.html')

@app.route('/set-symbol', methods=['POST'])
def set_symbol():
    """
    Handles the player's choice of symbol (X or O).
    Updates the global HUMAN and AI symbols and resets the game board.
    
    Expects a JSON payload with a 'symbol' key (e.g., {"symbol": "X"}).
    Returns a JSON response indicating success.
    """
    global HUMAN, AI, board # Declare global to modify the module-level variables.
    HUMAN = request.json['symbol'] # Get the chosen symbol from the request.
    AI = 'O' if HUMAN == 'X' else 'X' # Assign the opposite symbol to the AI.
    board = ['' for _ in range(9)] # Reset the board for a new game.
    return jsonify({'success': True})

@app.route('/make-move', methods=['POST'])
def make_move():
    """
    Handles a player's move or an AI-initiated first move.
    
    If 'position' is provided in the JSON payload, it's a human player's move.
    If 'position' is None, it signifies an AI's first move (e.g., if AI is 'X').
    
    Updates the board, checks for game-ending conditions, and if the game is still
    ongoing, calculates and makes the AI's counter-move.
    
    Returns a JSON response with the updated board state, game over status, winner,
    and the current player for the next turn.
    """
    position = request.json.get('position')
    
    # Scenario 1: AI makes the first move (e.g., if AI is 'X' and starts the game).
    if position is None:
        # Check if the board is already full, which would mean no AI move is possible.
        if '' not in board: 
            return jsonify({'error': 'Board is full, cannot make AI move'})
        
        # Get the best move for the AI using the minimax algorithm.
        ai_move = get_best_move(board)
        if ai_move is not None:
            board[ai_move] = AI # Apply the AI's move to the board.
        
        # Return the updated game state to the frontend.
        return jsonify({
            'board': board,
            'gameOver': check_winner(board) is not None,
            'winner': check_winner(board),
            'currentPlayer': HUMAN if check_winner(board) is None else None # If game not over, it's human's turn.
        })

    # Scenario 2: Human player makes a move.
    position = int(position) # Convert the position from string to integer.
    
    # Validate the move: ensure the chosen cell is empty.
    if board[position] == '':
        board[position] = HUMAN # Apply the human's move to the board.
        
        # After human's move, check if they won or if it's a tie.
        if check_winner(board):
            return jsonify({
                'board': board,
                'gameOver': True,
                'winner': check_winner(board),
                'currentPlayer': None # Game is over, no current player.
            })
            
        # If the game is not over, it's the AI's turn to make a counter-move.
        ai_move = get_best_move(board)
        if ai_move is not None:
            board[ai_move] = AI # Apply the AI's move.
            
        # Return the updated game state after AI's move to the frontend.
        return jsonify({
            'board': board,
            'gameOver': check_winner(board) is not None,
            'winner': check_winner(board),
            'currentPlayer': HUMAN if check_winner(board) is None else None # If game not over, it's human's turn.
        })
    
    # If the human tried to make an invalid move (e.g., clicked on an occupied cell).
    return jsonify({'error': 'Invalid move'})

# Entry point for running the Flask application.
if __name__ == '__main__':
    # Run the Flask app in debug mode, accessible from any IP address on port 5000.
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    app.run(debug=True, host="0.0.0.0", port=5000)
