import socket
import threading
import pickle
from time import sleep
from dotenv import load_dotenv
import os

from constants import TIMER

load_dotenv()
HOST = os.getenv('IP')
PORT = int(os.getenv('PORT'))

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()  # player 1 or 2
    
    
    def connect(self, timeout=5):
        self.client.settimeout(timeout)
        try:
            self.client.connect(self.addr)
            return int((self.client.recv(2048)).decode())
        except socket.timeout:
            print("[CONNECTION] Timeout expired. Connection failed")
            return -1
        except:
            return -1
    

    def disconnect(self, connection_state, in_game = True):
        print("[GAME] Multiplayer game ended\n")

        if in_game:
            connection_state["disconnected"] = True
            self.send("quit")
        else:
            connection_state["failed_connection"] = True

        self.client.close()
    

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)



class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    
#     def get_id(self):
#         # returns id of the respective thread
#         if hasattr(self, '_thread_id'):
#             return self._thread_id
#         for id, thread in threading._active.items():
#             if thread is self:
#                 return id
  

#     def raise_exception(self):  # function to terminate the thread
#         thread_id = self.get_id()
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
#               ctypes.py_object(SystemExit))
#         if res > 1:
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
#             print('Exception raise failure')



class ClientThread(MyThread):
    def __init__(self, client, connection_state, game_state, board):
        super().__init__()
        self.client = client
        self.connection_state = connection_state
        self.game_state = game_state
        self.board = board
    
    
    def run(self):
        while not self.connection_state["disconnected"]:

            if self.board.turn != self.game_state["my_color"]:  # constantly check for status if it is not your turn
                try:
                    data = self.client.send("status")  # 0 = still waiting, 1 = opponent disconnected, otherwise player did a move

                    if data == 1:
                        print("[GAME] Opponent disconnected")
                        self.connection_state["opponent_disconnected"] = True

                    elif data != 0:
                        new_fen_board, _ = data
                        splitted_fen = new_fen_board.split()
                        if self.game_state["my_color"] == "white":
                            my_color = "w"
                        else:
                            my_color = "b"
                        if splitted_fen[1] == my_color:  # if you received the board and now it is your turn
                            self.connection_state["new_data"] = data
                
                except:
                    print("[ERROR] Error in function run, class ClientThread, file client.py")
                    break
            

            else:  # constantly check if there is an opponent if it is your turn
                try:
                    data = self.client.send("opponent")  # 0 = everything ok, 1 = opponent disconnected
                    if data == 1:
                        print("[GAME] Opponent disconnected")
                        self.connection_state["opponent_disconnected"] = True

                except:
                    print("[ERROR] Error in function run, class ClientThread, file client.py")
                    break
            
            sleep(TIMER)



class ConnectionThread(MyThread):
    def __init__(self, connection_state, game_state, board):
        super().__init__()
        self.connection_state = connection_state
        self.game_state = game_state
        self.board = board
    
    
    def run(self):
        print("[CONNECTION] Starting connection thread")

        try:
            client = Client()
            if client.id == -1:  # could not connect with the server
                print("[CONNECTION] Could not connect to the server. Ending connection thread")
                client.disconnect(self.connection_state, in_game=False)

            else:
                self.game_state["my_color"] = "white" if client.id == 1 else "black"
                self.game_state["enemy_color"] = "black" if client.id == 1 else "white"
                self.connection_state["client"] = client
            
                client.send("myname" + self.game_state["my_name"])

                print("[CONNECTION] Waiting for an opponent...")
                while not self.connection_state["failed_connection"] and self.check_for_opponent(client) == False:
                    sleep(TIMER)
                
                if not self.connection_state["failed_connection"]:
                    print("[CONNECTION] Opponent found")
                    enemy_name = client.send("enemyname")  # get the name of the enemy from the server
                    self.game_state["enemy_name"] = enemy_name

                    client_thread = ClientThread(client, self.connection_state, self.game_state, self.board)
                    client_thread.start()
                    self.connection_state["client_thread"] = client_thread
            
                    print("[CONNECTION] Ending connection thread successfully")
                
                else:
                    print("[CONNECTION] Could not connect to the server. Ending connection thread")
                    client.disconnect(self.connection_state, in_game=False)
        
        except:
            print("[CONNECTION] Could not connect to the server. Ending connection thread")
            self.connection_state["failed_connection"] = True
    
    
    def check_for_opponent(self, client):
        response = client.send("start")
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            raise Exception("Error in function check_for_opponent in file multi_player.py")