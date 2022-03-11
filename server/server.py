import socket
import _thread
import pickle
import re


with open("server_ip.txt", "r") as f:
    line1 = f.readline()
    line2 = f.readline()

host_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
port_pattern = re.compile(r'(\d{1,5})')
HOST = re.search(host_pattern, line1)[0]
PORT = int(re.search(port_pattern, line2)[0])


MAX_GAMES = 3 # <--- change this value to change the max number of games that the server can handle

PLAYERS_CONNECTED = [{1: None, 2: None} for _ in range(MAX_GAMES)]
NEW_BOARD = [{1: None, 2: None} for _ in range(MAX_GAMES)]
# when the new_board is not None, the corresponding player has not read it. New_board expressed in fen notation.

##########################################################################################

def threaded_client(conn, address, game_index, current_player):
    print(f"\n\nSending player {current_player} {address} in game {game_index+1}")
    conn.send(str(current_player).encode()) # sends to the client if he is player 1 or player 2
    
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # stuck here until the client sends some data
            
            if not data:
                break
            
            elif data[:6] == "myname":  # user sends his name to the server
                PLAYERS_CONNECTED[game_index][current_player] = data[6:]
                conn.sendall(pickle.dumps("received"))
            
            elif data == "enemyname":  # user asks for the enemy name
                if current_player == 1:
                    conn.sendall(pickle.dumps(PLAYERS_CONNECTED[game_index][2]))
                else:
                    conn.sendall(pickle.dumps(PLAYERS_CONNECTED[game_index][1]))
            
            elif data == "start":  # user asks if the game has started
                if PLAYERS_CONNECTED[game_index][1] and PLAYERS_CONNECTED[game_index][2]:
                    conn.sendall(pickle.dumps('y'))
                else:
                    conn.sendall(pickle.dumps('n'))
            
            elif data == "quit":  # user quits
                conn.sendall(pickle.dumps(0))
                break
                
            elif data == "status":  # user asks if now it is his turn
                if NEW_BOARD[game_index][current_player] != None:
                    conn.sendall(pickle.dumps(NEW_BOARD[game_index][current_player]))
                    NEW_BOARD[game_index][current_player] = None
                else:
                    conn.sendall(pickle.dumps(0))
            
            else:  # user sends the new fen board
                print(f"Player {current_player} in game {game_index+1} did a move")
                print("Changing the turn to the other player")
                NEW_BOARD[game_index][1] = data
                NEW_BOARD[game_index][2] = data
                conn.sendall(pickle.dumps("received"))
             
        except:
            break

    PLAYERS_CONNECTED[game_index][current_player] = None
    NEW_BOARD[game_index][current_player] = None
    print(f"\n\nLost connection with player {current_player} {address} in game {game_index+1}")
    conn.close()
    
##########################################################################################
    
def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
    except socket.error as e:
        print("Server creation failed with error %s" %(e))

    server.listen(2)  # there can be a maximum of 2 users in the queue
    print("Server started on", (HOST, PORT))
    print("Waiting for a connection...")

    
    while True:
        conn, address = server.accept()  # stuck here until a new user connects to the server

        for game_index in range(MAX_GAMES):
            
            if not PLAYERS_CONNECTED[game_index][1]:
                PLAYERS_CONNECTED[game_index][1] = "guest"
                # calls threaded_client that start its execution in the background
                _thread.start_new_thread(threaded_client, (conn, address, game_index, 1))
                break
            
            if not PLAYERS_CONNECTED[game_index][2]:
                PLAYERS_CONNECTED[game_index][2] = "guest"
                # calls threaded_client that start its execution in the background
                _thread.start_new_thread(threaded_client, (conn, address, game_index, 2))
                break
               
        else:
            print(f"\n\nCould not connect with {address}: there are alreay {MAX_GAMES*2} players playing")
            conn.close()