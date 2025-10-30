# Unbeatable Tic-Tac-Toe AI

This project features an interactive web-based Tic-Tac-Toe game where a human player can challenge an unbeatable AI opponent. The AI is powered by the **Minimax algorithm with Alpha-Beta pruning**, ensuring optimal play and an unwinnable experience for the human player.

## Overview

This application provides a classic Tic-Tac-Toe experience against an intelligent AI. The game is played through a web browser, offering a clean and responsive interface. Players can choose their symbol and engage in a strategic battle against an AI that always makes the optimal move, guaranteeing at least a draw.

## Features

*   **Unbeatable AI:** Implemented using the Minimax algorithm with Alpha-Beta pruning for optimal decision-making.
*   **Web-Based Interface:** Play directly in your browser with a responsive and intuitive user interface.
*   **Player Choice:** Select to play as either 'X' or 'O'.
*   **Real-time Game State:** Clear display of the current board, game status (win, lose, draw), and whose turn it is.
*   **Game Reset:** Easily start a new game at any time.

## Technologies Used

*   **Backend:** Python (Flask)
*   **Frontend:** HTML, CSS, JavaScript
*   **AI Algorithm:** Minimax with Alpha-Beta Pruning

## Project Structure and File Contents

*   `app.py`: This is the Flask backend application. It contains all the core game logic, including the implementation of the Minimax algorithm with Alpha-Beta pruning. It defines the API endpoints that handle player moves, symbol selection, and game state management.
*   `templates/index.html`: This file constitutes the frontend of the web application. It includes the HTML structure for the game board, embedded CSS for styling, and JavaScript for client-side interactivity. The JavaScript handles user input, updates the game board visually, and communicates with the Flask backend via API calls.
*   `.gitignore`: Specifies intentionally untracked files and directories that Git should ignore.
*   `README.md`: This file, providing a comprehensive overview, setup instructions, and details about the project.
*   `requirements.txt`: Lists the Python dependencies required for the project.

## Quick Run

Follow these steps to set up and run the game locally:

1.  **Install Dependencies:**

    Ensure you have Python and `pip` installed. Then, install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application:**

    ```bash
    python app.py
    ```

3.  **Access the Game:**

    Open your web browser and navigate to `http://localhost:5000`.

## The Algorithm: Minimax with Alpha-Beta Pruning

This AI employs the **Minimax algorithm** to determine the optimal move. Minimax is a recursive algorithm used in decision-making and game theory, where the AI (maximizing player) aims to maximize its score, while assuming the opponent (minimizing player) will always choose moves that minimize the AI's score. It explores all possible game states to find the best path.

To enhance performance, **Alpha-Beta Pruning** is integrated. This optimization technique significantly reduces the number of nodes evaluated by the Minimax algorithm. It works by intelligently cutting off branches in the game tree that cannot possibly influence the final decision, thereby speeding up the AI's move calculation without compromising its optimal play.

## Contributions

Feel free to submit issues, feature requests, or contribute to the codebase. All contributions are welcome!