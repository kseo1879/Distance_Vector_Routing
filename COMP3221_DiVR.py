from _thread import *
import threading
import _thread
import time
import socket
import sys
import json
import copy

IP = "127.0.0.1"

BUFFER_SIZE = 1024
FREQUENCY = 10 # seceonds it sends information to neibouring nodes.

NODE_INDEX = 0
DISTANCE_INDEX = 1
PORT_INDEX = 2
DIR_INDEX = 3


class Node:
    def __init__(self, nodeId, portNo, configFile):
        self.nodeId = nodeId
        self.portNo = portNo
        self.configFile = configFile
        self.terminated = False #This can come useful when we need to determine the failed node
        self.finishedChanging = False
        self.printed = False
        self.noNeighbour = 0
        self.neighbour = [] #Stores the neigbour information //nodeId, port_no
        self.routeTable = [] # Stores the routing table of the current node

        self.l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.l_socket.bind((IP, self.portNo))
        self.l_socket.listen(5)

        #Mutexes
        self.sendLock = threading.Lock()

        #Saving information to the routeTable and neighbour Table
        try:
            file = open(self.configFile, "r")
            file_line = file.read().split("\n")
            self.noNeighbour = int(file_line[0])

            # It has to have it self at the routing table.
            temp = []
            temp.append(self.nodeId)
            temp.append('0')
            temp.append(str(self.portNo))
            temp.append("local")
            self.routeTable.append(temp)

            for i in range(0, self.noNeighbour):
                temp2 = file_line[i + 1].split(" ")
                self.neighbour.append(copy.deepcopy(temp2))
                dir_parent = ""+temp2[0]
                temp2.append(dir_parent)
                self.routeTable.append(temp2)

        except Exception as e:
            print("There is an error: ")
            print(e)

    def route(self, table):
        length_route = len(self.routeTable)
        for i in range(1, len(table)):
            found = False
            indexOfRouteTable = -1
            indexofTable = -1
            if(self.routeTable[0][NODE_INDEX] == table[i][NODE_INDEX]):
                continue
            for j in range(1, length_route):
                if(self.routeTable[j][NODE_INDEX] == table[i][NODE_INDEX]):
                    found = True
                    indexOfRouteTable = j
                if(self.routeTable[j][NODE_INDEX] == table[0][NODE_INDEX]):
                    indexofTable = j               
            if found:
                #This means that the key already exsitest in the routing table
                if float(table[i][DISTANCE_INDEX]) + float(self.routeTable[indexofTable][DISTANCE_INDEX]) < float(self.routeTable[indexOfRouteTable][DISTANCE_INDEX]):
                    self.routeTable[indexOfRouteTable][DISTANCE_INDEX] = str(float(table[i][DISTANCE_INDEX]) + float(self.routeTable[indexofTable][DISTANCE_INDEX]))
                    # self.routeTable[indexOfRouteTable][DIR_INDEX] = table[0][NODE_INDEX] + self.routeTable[indexOfRouteTable][DIR_INDEX]
                    self.routeTable[indexOfRouteTable][DIR_INDEX] = str(table[0][NODE_INDEX] + table[i][DIR_INDEX])
                    self.finishedChanging = False
                    self.printed = False
                else:
                    self.finishedChanging = True
                
            else:
                #It means that there is no such node in the routing table yet
                self.routeTable.append(
                    [str(table[i][NODE_INDEX]), 
                    str(float(table[i][DISTANCE_INDEX]) + float(self.routeTable[indexofTable][DISTANCE_INDEX])), 
                    str(table[i][PORT_INDEX]), 
                    str(table[0][NODE_INDEX] + table[i][DIR_INDEX])])
                    
                self.finishedChanging = False
                self.printed = False

    def listen_update(self, c, addr):
        while True:
            data_rev = c.recv(1024)
            data_rev = data_rev.decode()

            table = json.loads(data_rev)
            self.sendLock.acquire()

            self.route(table)
            self.sendLock.release()

        c.close()

    def listen(self):
        try:
            while True:
                c, addr = self.l_socket.accept()
                _thread.start_new_thread(self.listen_update,(c, addr))
            l_socket.close()
        except:
            print("Can't connect to the Socket when listening")

    def send_update(self, index):
        while(1):
            time.sleep(1)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#s = socket.socket()         # Create a socket object
                    s.connect((IP, int(self.neighbour[int(index)][PORT_INDEX])))
                    while(1):
                        time.sleep(FREQUENCY)
                        self.sendLock.acquire()
                        msg = json.dumps(self.routeTable)
                        msg = str.encode(msg)
                        s.sendall(msg)

                        self.sendLock.release()
                    s.close()   
            except Exception as e:
                print("", end = "")

    def send(self):
        for i in range(self.noNeighbour):
            thread = threading.Thread(target=self.send_update, args=(str(i)))
            thread.start()
        return

    def printRoute(self):
        while(1):
            time.sleep(1)
            if not self.printed:
                if(self.finishedChanging):
                    self.sendLock.acquire()
                    self.routeTable[1:].sort()
                    print("I am node " + self.nodeId)
                    for i in range(1, len(self.routeTable)):
                        msg = f"Least cost path from {self.nodeId} to {self.routeTable[i][NODE_INDEX]}: {self.nodeId}{self.routeTable[i][DIR_INDEX]}: {self.routeTable[i][DISTANCE_INDEX]}"
                        print(msg)
                    self.printed = True
                    print(" ")
                    self.sendLock.release()
                    time.sleep(FREQUENCY)
        
    def run(self):
        listeningThread = threading.Thread(target=self.listen)
        listeningThread.start()
        sendingThread = threading.Thread(target=self.send)
        sendingThread.start()
        routePrintThread = threading.Thread(target=self.printRoute)
        routePrintThread.start()

if __name__ == "__main__":
    try:
        #Get input from the user. ex) python3 F 6005 Fconfig.txt
        nodeId = sys.argv[1]
        portNo = int(sys.argv[2])
        configFile = sys.argv[3]
        node = Node(nodeId, portNo, configFile)
        node.run()

    except Exception as e:
        print("There is an error: ")
        print(e)