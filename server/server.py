import socket
import _thread
import pickle
import time
from dotenv import load_dotenv
import os


load_dotenv()
HOST = ''
PORT = int(os.getenv('PORT'))


MAX_GAMES = 3 # <--- change this value to change the max number of games that the server can handle
LOG_TIMER = 10  # time between logs on terminal in seconds
DISCONNECT_TIMER = 15  # close the connection with a client if no data is received in this time

PLAYERS_CONNECTED = [{1: None, 2: None} for _ in range(MAX_GAMES)]
NEW_BOARD = [{1: None, 2: None} for _ in range(MAX_GAMES)]
# when the new_board is not None, the corresponding player has not read it. New_board expressed in fen notation


def threaded_client(conn, address, game_index, current_player):
    print(f"[CONNECT] Sending player {current_player} {address} in game {game_index+1}")
    conn.send(str(current_player).encode()) # sends to the client if he is player 1 or player 2
    conn.settimeout(DISCONNECT_TIMER)
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # stuck here until the client sends some data
            
            if not data:
                break
            
            # USER SENDS HIS NAME TO THE SERVER
            elif data[:6] == "myname":
                PLAYERS_CONNECTED[game_index][current_player] = data[6:]
                conn.sendall(pickle.dumps("received"))
            
            # USER ASKS FOR THE ENEMY NAME
            elif data == "enemyname":
                if current_player == 1:
                    conn.sendall(pickle.dumps(PLAYERS_CONNECTED[game_index][2]))
                else:
                    conn.sendall(pickle.dumps(PLAYERS_CONNECTED[game_index][1]))
            
            # USER ASKS IF THE GAME HAS STARTED
            elif data == "start":
                if PLAYERS_CONNECTED[game_index][1] and PLAYERS_CONNECTED[game_index][2]:
                    conn.sendall(pickle.dumps('y'))
                else:
                    conn.sendall(pickle.dumps('n'))
            
            # USER IS QUITTING
            elif data == "quit":
                conn.sendall(pickle.dumps(0))
                break
            
            # USER ASKS FOR STATUS (if it is not his turn)
            elif data == "status":
                if NEW_BOARD[game_index][current_player] != None:
                    conn.sendall(pickle.dumps(NEW_BOARD[game_index][current_player]))
                    NEW_BOARD[game_index][current_player] = None
                elif PLAYERS_CONNECTED[game_index][1] and PLAYERS_CONNECTED[game_index][2]:
                    conn.sendall(pickle.dumps(0))  # there are still 2 players in the game
                else:
                    conn.sendall(pickle.dumps(1))  # a player left
            
            # USER ASKS IF THERE IS STILL AN OPPONENT (if it is his turn)
            elif data == "opponent":
                if PLAYERS_CONNECTED[game_index][1] and PLAYERS_CONNECTED[game_index][2]:
                    conn.sendall(pickle.dumps(0))  # there are still 2 players in the game
                else:
                    conn.sendall(pickle.dumps(1))  # a player left
            
            # USER SENDS THE NEW FEN BOARD
            else:
                #print(f"Player {current_player} in game {game_index+1} did a move")
                #print("Changing the turn to the other player")
                NEW_BOARD[game_index][1] = data
                NEW_BOARD[game_index][2] = data
                conn.sendall(pickle.dumps("received"))
             
        except:
            break

    PLAYERS_CONNECTED[game_index][current_player] = None
    NEW_BOARD[game_index][1] = None
    NEW_BOARD[game_index][2] = None
    print(f"[DISCONNECT] Lost connection with player {current_player} {address} in game {game_index+1}")
    conn.close()


def threaded_log(timer):
    while True:
        print(f"[LOG] Players connected: {PLAYERS_CONNECTED}")
        print(f"[LOG] New boards: {NEW_BOARD}")
        time.sleep(timer)
    

    
def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
    except socket.error as e:
        print("[ERROR] Server creation failed with error %s" %(e))

    server.listen(4)  # there can be a maximum of 4 users in the queue
    print("[START] Server started on", (HOST, PORT))
    print("[START] Waiting for a connection...")

    _thread.start_new_thread(threaded_log, (LOG_TIMER,))

    
    while True:
        conn, address = server.accept()  # stuck here until a new user connects to the server

        for game_index in range(MAX_GAMES):
            
            if not PLAYERS_CONNECTED[game_index][1]:
                PLAYERS_CONNECTED[game_index][1] = "guest"
                _thread.start_new_thread(threaded_client, (conn, address, game_index, 1))
                break
            
            if not PLAYERS_CONNECTED[game_index][2]:
                PLAYERS_CONNECTED[game_index][2] = "guest"
                _thread.start_new_thread(threaded_client, (conn, address, game_index, 2))
                break
               
        else:
            print(f"[WARNING] Could not connect with new player {address}: there are alreay {MAX_GAMES*2} players playing")
            conn.close()



if __name__ == "__main__":
    run()