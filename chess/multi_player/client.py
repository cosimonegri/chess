import socket
import threading
import pickle
import ctypes
import re
from time import sleep
from constants import TIMER


with open("server_ip.txt", "r") as f:
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()

if re.search(r'true', line1) != None:
    host_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    port_pattern = re.compile(r'(\d{1,5})')
    HOST = re.search(host_pattern, line2)[0]
    PORT = int(re.search(port_pattern, line3)[0])
else:
    HOST = "34.65.155.95"
    PORT = 3389


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()  # player 1 or 2
    
    def connect(self):
        self.client.settimeout(5)
        try:
            self.client.connect(self.addr)
            return int((self.client.recv(2048)).decode())
        except socket.timeout:
            print("Timeout expired")
            return -1
        except:
            return -1
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)



class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  

    def raise_exception(self):  # function to terminate the thread
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')



class ClientThread(MyThread):
    def __init__(self, client, board, connection_state, game_state):
        super().__init__()
        self.client = client
        self.board = board
        self.connection_state = connection_state
        self.game_state = game_state
    
    
    def run(self):
        while not self.connection_state["disconnecting"]:
            if self.board.turn != self.game_state["my_color"]:  # constantly check for status if it is not your turn
                
                try:
                    data = self.client.send("status")  # 0 = still waiting, 1 = player disconnected, otherwise player did a move
                    print(data)

                    if data == 1:
                        self.connection_state["opponent_disconnected"] = True

                    elif data != 0:
                        new_fen_board, new_eaten_pieces = data
                        splitted_fen = new_fen_board.split()
                        
                        if self.game_state["my_color"] == "white":
                            my_color = "w"
                        else:
                            my_color = "b"
                        
                        if splitted_fen[1] == my_color:  # if you received the board and now it is your turn
                            self.connection_state["new_data"] = data
                    
                    sleep(TIMER)
                except:
                    break
            
            else:
                sleep(3)



class ConnectionThread(MyThread):
    def __init__(self, connection_state, game_state, board):
        super().__init__()
        self.connection_state = connection_state
        self.game_state = game_state
        self.board = board
    
    
    def run(self):

        try:
            client = Client()
            if client.id == -1:  # could not connect with the server
                self.connection_state["failed_connection"] = True
            else:
                self.game_state["my_color"] = "white" if client.id == 1 else "black"
                self.game_state["enemy_color"] = "black" if client.id == 1 else "white"
                self.connection_state["client"] = client
            

            if not self.connection_state["failed_connection"]:
                message = "myname" + self.game_state["my_name"]
                response = client.send(message)
                if response != "received":
                    print("Trying again to send my name to the server")
                    response = client.send(message)
                
                print("Waiting for an opponent...")
                while not self.connection_state["failed_connection"] and self.check_for_opponent(client) == False:
                    sleep(TIMER)
                
                if not self.connection_state["failed_connection"]:
                    print("Opponent found")
                    enemy_name = client.send("enemyname")
                    self.game_state["enemy_name"] = enemy_name
                    client_thread = ClientThread(client, self.board, self.connection_state, self.game_state)
                    client_thread.start()
                    self.connection_state["client_thread"] = client_thread
            
            print("successfully end connection thread")
        
        except:
            print("killing conenction thread")
    
    
    def check_for_opponent(self, client):
        response = client.send("start")
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            raise Exception("error in function check_for_opponent in file multi_player.py")