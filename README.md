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

If you want to install the packages in a virtual environment, create it and activate it.

Finally, no matter if you decided to go for the virtual environment or no, run the following command in the chess folder:

    pip install -r requirements.txt

# To make the game work...

### _Singleplayer_

Just run the following command in the chess folder:

    python3.10 chess

### _Multiplayer_

Before running any script, edit the ip and the port of the server in the **.env** file. This is a hidden file, so if you don't see it, search on the internet how to see hidden files in your operative system.

- **IP**: replace the ip with the one of the machine where you are going to run the server. Make sure to obtain a line that has exactly the form _IP = x.x.x.x_ without extra spaces, where x is a number between 0 and 255.

  If the server is on the same machine where you are going to play, replace the IP line in the file with:

        IP = localhost

- **PORT**: you can leave this unchanged. But if you want to change it, make sure to obtain a line that has exactly the form _PORT = x_ without extra spaces, where x is a number between 1024 and 49151.

Now everything is setted up to start using the game.

Run the following command in the chess folder to run the server:

    python3.10 server

Run the following command in the chess folder to run the client (game):

    python3.10 chess

# Screenshots

### Main menu

![Main menu image](/screenshots/screen1?raw=True)

### In game

![Game menu image](/screenshots/screen2?raw=True)

# More

### _Singleplayer_

The bot is implemented through a minimax algorithm, with alpha-beta pruning and move ordering for optimization. It sees four moves in the future, and chooses the move that leads to the best table for him. Each table is evaluated through material and pieces positions on the board.

### _Multiplayer_

The server script handles the connections between the players, and during the game it forwards the move received from a player to the other. The client scripts handle the user interface and the game logic.
