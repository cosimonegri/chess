import socket
import _thread
import pickle
import time
from dotenv import load_dotenv
import os


class Server():
    """Server class to put the clients in communication.

    :attr players: list[dict[ int, optional[str] ]]
    :attr boards: list[dict[ int, optional[str] ]]
    :attr host: str
    :attr port: int
    """

    MAX_GAMES = 3
    LOG_TIMER = 10  # time between logs on terminal in seconds
    DISCONNECT_TIMER = 5  # close the connection with a client if no data is received in this time


    def __init__(self, port):
        """
        :param port: int
        """
        # It contains None or the name of the player
        self.players = [{1: None, 2: None} for _ in range(self.MAX_GAMES)]

        # When a board is not None, the corresponding player has not read it yet
        self.boards = [{1: None, 2: None} for _ in range(self.MAX_GAMES)]

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''
        self.port = port
    

    def run(self, listen_num=4):
        """Handles the initial phase of the connection with clients.

        Never ending loop, in which the server listens for clients and accepts them if there is a free space in a game.
        The actual communication with the client is handled by the function: threaded_client.

        :param listen_num: int
        :return: None
        """
        try:
            self.server.bind((self.host, self.port))
        except socket.error as e:
            print("[ERROR] Server creation failed with error %s" %(e))

        self.server.listen(listen_num)
        print("[START] Server started on", (self.host, self.port))
        print("[START] Waiting for a connection...")

        _thread.start_new_thread(self.threaded_log, ())

        while True:
            conn, address = self.server.accept()  # stuck here until a new user connects to the server

            for game_id in range(self.MAX_GAMES):
                if not self.players[game_id][1]:
                    self.players[game_id][1] = "guest"
                    _thread.start_new_thread(self.threaded_client, (conn, address, game_id, 1))
                    break
                if not self.players[game_id][2]:
                    self.players[game_id][2] = "guest"
                    _thread.start_new_thread(self.threaded_client, (conn, address, game_id, 2))
                    break
                
            else:
                print(f"[WARNING] Could not connect with new player {address}: \
                        there are alreay {self.MAX_GAMES*2} players playing")
                conn.close()
    

    def threaded_log(self, timer=LOG_TIMER):
        """Prints every now and then the state of the current connections.

        It runs in the background, as a thread.

        :param timer: int
        :return: None
        """
        while True:
            print(f"[LOG] Players connected: {self.players}")
            time.sleep(timer)


    def threaded_client(self, conn, address, game_id, player_id):
        """Handles the communication between the server and a specific client.

        It runs in the background, as a thread.
        
        :param conn: socket.Socket
        :param address: tuple[str, int]
        :param game_id: int
        :param player_id: int
        :return: None
        """
        print(f"[CONNECT] Sending player {player_id} {address} in game {game_id+1}")
        conn.send(str(player_id).encode()) # sends to the client if he is player 1 or player 2
        conn.settimeout(self.DISCONNECT_TIMER)
        
        while True:
            try:
                data = pickle.loads(conn.recv(2048))  # stuck here until the client sends some data
                
                if not data:
                    break
                
                # USER SENDS HIS NAME TO THE SERVER
                elif data[:6] == "myname":
                    self.players[game_id][player_id] = data[6:]
                    conn.sendall(pickle.dumps("received"))
                
                # USER ASKS FOR THE ENEMY NAME
                elif data == "enemyname":
                    if player_id == 1:
                        conn.sendall(pickle.dumps(self.players[game_id][2]))
                    else:
                        conn.sendall(pickle.dumps(self.players[game_id][1]))
                
                # USER ASKS IF THE GAME HAS STARTED
                elif data == "start":
                    if self.players[game_id][1] and self.players[game_id][2]:
                        conn.sendall(pickle.dumps('y'))
                    else:
                        conn.sendall(pickle.dumps('n'))
                
                # USER IS QUITTING
                elif data == "quit":
                    conn.sendall(pickle.dumps(0))
                    break
                
                # USER ASKS FOR STATUS (if it is not his turn)
                elif data == "status":
                    if self.boards[game_id][player_id] != None:
                        conn.sendall(pickle.dumps(self.boards[game_id][player_id]))
                        self.boards[game_id][player_id] = None
                    elif self.players[game_id][1] and self.players[game_id][2]:
                        conn.sendall(pickle.dumps(0))  # there are still 2 players in the game
                    else:
                        conn.sendall(pickle.dumps(1))  # a player left
                
                # USER ASKS IF THERE IS STILL AN OPPONENT (if it is his turn)
                elif data == "opponent":
                    if self.players[game_id][1] and self.players[game_id][2]:
                        conn.sendall(pickle.dumps(0))  # there are still 2 players in the game
                    else:
                        conn.sendall(pickle.dumps(1))  # a player left
                
                # USER SENDS THE NEW FEN BOARD
                else:
                    self.boards[game_id][1] = data
                    self.boards[game_id][2] = data
                    conn.sendall(pickle.dumps("received"))
                
            except:
                break

        self.players[game_id][player_id] = None
        self.boards[game_id][1] = None
        self.boards[game_id][2] = None
        print(f"[DISCONNECT] Lost connection with player {player_id} {address} in game {game_id+1}")
        conn.close()



if __name__ == "__main__":
    load_dotenv()
    PORT = int(os.getenv('PORT'))

    server = Server(PORT)
    server.run()