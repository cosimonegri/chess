# Python Chess Game

A chess game that supports both singleplayer against a bot and multiplayer against a random opponent.

The game was created using:

- **Python 3.10**
- **Pygame** module for the user interface
- **Socket** module for the client-server connection

# Installation

If you don't have python3 installed, follow the instructions [here](https://www.python.org/downloads/).

Then, in the directory where you want to download the game, run the following commands:

    git clone https://github.com/cosimonegri/chess.git
    cd chess
    pip install -r requirements.txt

# To make the game work...

Edit the file **server_ip.txt** with the ip and the port of the server.

To run the server:

    python3 server

To run the client:

    python3 client

# Screenshots

## Main menu

![Main menu image](/screenshots/screen1?raw=True)

## In game

![Game menu image](/screenshots/screen2?raw=True)

# More

## - Singleplayer

The bot is implemented through a minimax algorithm, with alpha-beta pruning and move ordering for optimization. It sees four moves in the future, and choose the move that leads to the best table for him. Each table is evaluated through material and pieces positions on the board.

## - Multiplayer

The server script handles the connections between the players, and during the game it forwards the move received from a player to the other. The client scripts handel the user interface and the game logic.
